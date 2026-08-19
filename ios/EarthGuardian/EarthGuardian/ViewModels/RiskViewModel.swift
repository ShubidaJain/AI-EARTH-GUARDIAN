import Foundation
import Combine

@MainActor
final class RiskViewModel: ObservableObject {

    @Published var prediction: PredictionResponse?

    @Published var isLoading = false

    @Published var errorMessage: String?
    
    @Published var gridPredictions:
        [GridPrediction] = []

    @Published var isLoadingGrid = false

    func fetchRisk(
        latitude: Double,
        longitude: Double
    ) {

        print("🚀 Starting prediction request")

        isLoading = true
        errorMessage = nil

        Task {

            do {

                print("📡 Calling FastAPI...")

                let result =
                    try await APIService.shared
                    .predictLive(
                        latitude: latitude,
                        longitude: longitude
                    )

                print("✅ Response received")

                print(
                    "Probability:",
                    result.prediction.fireProbability
                )

                print(
                    "Risk:",
                    result.prediction.riskLevel
                )

                prediction = result

            } catch {

                print("❌ Prediction error:")
                print(error)

                if let urlError =
                    error as? URLError {

                    print(
                        "URLError:",
                        urlError.code
                    )

                    print(
                        "Description:",
                        urlError.localizedDescription
                    )
                }

                errorMessage =
                    error.localizedDescription
            }

            isLoading = false

            print("🏁 Request finished")
        }
    }
    func fetchGrid(
        latitude: Double,
        longitude: Double
    ) {

        print("🗺️ Starting grid prediction")

        isLoadingGrid = true

        Task {

            do {

                let response =
                    try await APIService.shared
                    .predictGrid(
                        latitude: latitude,
                        longitude: longitude,
                        radius: 0.5,
                        points: 5
                    )

                print(
                    "✅ Grid received:",
                    response.count,
                    "cells"
                )

                gridPredictions =
                    response.results

            } catch {

                print(
                    "❌ Grid prediction error:",
                    error
                )
            }

            isLoadingGrid = false

            print("🏁 Grid request finished")
        }
    }
}

