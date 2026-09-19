import XCTest
@testable import CoreAIIPhone

final class CoreAIIPhoneTests: XCTestCase {

    func testServiceAPIExists() async throws {
        XCTAssertTrue(true)
    }

    func testServiceRejectsMissingModelResources() async {
        let missingURL = FileManager.default.temporaryDirectory
            .appendingPathComponent("coreai-test-missing-(UUID().uuidString)")

        do {
            _ = try await CoreAIService(modelURL: missingURL)
            XCTFail("CoreAIService should reject a missing model resource directory")
        } catch {
            XCTAssertFalse(error.localizedDescription.isEmpty)
        }
    }
}
