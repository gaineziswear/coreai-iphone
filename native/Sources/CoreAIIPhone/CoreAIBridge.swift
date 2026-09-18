import Foundation
import FoundationModels
import CoreAILanguageModels

public enum CoreAIRuntimeState: Sendable {
    case unloaded
    case initialized
    case loading
    case ready
    case generating
    case failed(String)
}

public actor CoreAIBridge {

    private let model: CoreAILanguageModel
    private let session: LanguageModelSession

    private(set) var state: CoreAIRuntimeState = .initialized

    public init(modelURL: URL) async throws {

        self.model = try await CoreAILanguageModel(
            resourcesAt: modelURL,
            mode: .lazy
        )

        self.session = LanguageModelSession(
            model: self.model
        )
    }

    public var estimatedSizeOnDiskBytes: Int? {
        model.estimatedSizeOnDiskBytes
    }

    public func load() async throws {

        guard state != .ready else {
            return
        }

        state = .loading

        do {
            try await model.load()
            state = .ready
        } catch {
            state = .failed(error.localizedDescription)
            throw error
        }
    }

    public func unload() {

        model.unload()
        state = .unloaded
    }

    public func respond(to prompt: String) async throws -> String {

        if state != .ready {
            try await load()
        }

        state = .generating

        do {

            let response = try await session.respond(
                to: prompt
            )

            state = .ready

            return response.content

        } catch {

            state = .failed(
                error.localizedDescription
            )

            throw error
        }
    }

    public func currentState() -> CoreAIRuntimeState {
        state
    }
}
