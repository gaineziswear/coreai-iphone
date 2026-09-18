import Foundation

public actor CoreAIService {

    private let bridge: CoreAIBridge

    public init(modelURL: URL) async throws {
        self.bridge = try await CoreAIBridge(
            modelURL: modelURL
        )
    }

    public func start() async throws {
        try await bridge.load()
    }

    public func stop() async {
        await bridge.unload()
    }

    public func ask(_ prompt: String) async throws -> String {
        try await bridge.respond(to: prompt)
    }

    public func modelSize() async -> Int? {
        await bridge.estimatedSizeOnDiskBytes
    }

    public func status() async -> CoreAIRuntimeState {
        await bridge.currentState()
    }
}
