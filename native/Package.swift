// swift-tools-version: 6.0

import PackageDescription

let package = Package(
    name: "CoreAIIPhone",
    platforms: [
        .iOS("27.0"),
        .macOS("27.0")
    ],
    products: [
        .library(
            name: "CoreAIIPhone",
            targets: [
                "CoreAIIPhone"
            ]
        )
    ],
    dependencies: [
    .package(
    url: "https://github.com/apple/coreai-models.git",
    branch: "main"
        )
    ],
    targets: [
        .target(
            name: "CoreAIIPhone",
            dependencies: [
                .product(
                    name: "CoreAILM",
                    package: "coreai-models"
                )
            ],
            path: "Sources/CoreAIIPhone"
        ),
        .testTarget(
            name: "CoreAIIPhoneTests",
            dependencies: [
                "CoreAIIPhone"
            ],
            path: "Tests/CoreAIIPhoneTests"
        )
    ]
)
