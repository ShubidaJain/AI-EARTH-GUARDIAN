import SwiftUI
import CoreLocation

struct ContentView: View {

    @StateObject private var viewModel =
        RiskViewModel()

    @StateObject private var locationManager =
        LocationManager()

    var body: some View {

        NavigationStack {

            ScrollView {

                VStack(spacing: 20) {

                    // Header

                    VStack(spacing: 5) {

                        Text("🌍")
                            .font(.system(size: 45))

                        Text("Earth Guardian")
                            .font(.largeTitle)
                            .bold()

                        Text(
                            "AI-powered wildfire protection"
                        )
                        .foregroundStyle(
                            .secondary
                        )
                    }


                    // Map

                    if let location =
                        locationManager.location {

                        MapView(
                            location: location,
                            gridPredictions: viewModel.gridPredictions,
                            gridRadius: viewModel.gridRadius,
                            gridPoints: viewModel.gridPoints
                        )
                        .frame(height: 300)
                        
                        if !viewModel.gridPredictions.isEmpty {
                            GridRiskSummaryView(
                                predictions: viewModel.gridPredictions
                            )
                        }

                        Text(
                            "📍 \(location.coordinate.latitude, specifier: "%.4f"), \(location.coordinate.longitude, specifier: "%.4f")"
                        )
                        .font(.caption)
                        .foregroundStyle(
                            .secondary
                        )
                    }


                    // Prediction

                    if let prediction =
                        viewModel.prediction {

                        RiskCardView(
                            prediction: prediction
                        )
                    }


                    // Loading

                    if viewModel.isLoading {

                        ProgressView(
                            "Analyzing fire risk..."
                        )
                    }
                    
                    if viewModel.isLoadingGrid {
                        ProgressView("Generating risk map...")
                    }


                    // Error

                    if let error =
                        viewModel.errorMessage {

                        Text(error)
                            .foregroundStyle(.red)
                            .multilineTextAlignment(
                                .center
                            )
                    }


                    // Buttons

                    if locationManager.location == nil {

                        Button(
                            "Allow Location Access"
                        ) {

                            locationManager
                                .requestPermission()
                        }
                        .buttonStyle(
                            .borderedProminent
                        )

                    } else {

                        Button("🔥 Analyze Current Location") {

                            guard let location =
                                    locationManager.location
                            else {
                                return
                            }

                            let latitude =
                                location.coordinate.latitude

                            let longitude =
                                location.coordinate.longitude

                            viewModel.fetchRisk(
                                latitude: latitude,
                                longitude: longitude
                            )

                            viewModel.fetchGrid(
                                latitude: latitude,
                                longitude: longitude
                            )
                        }
                        .buttonStyle(.borderedProminent)
                    }
                }
                .padding()
            }
        }
    }
}

