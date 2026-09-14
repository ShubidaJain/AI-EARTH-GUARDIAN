//
//  RiskDetailView.swift
//  EarthGuardian
//
//  Created by CU_Student26 on 07/09/26.
//

import SwiftUI

struct RiskDetailView: View {
    
    let prediction: GridPrediction
    
    private var riskColor: Color {
        switch prediction.prediction.riskLevel.uppercased() {
        case "LOW":
            return .green
        case "MODERATE":
            return .yellow
        case "HIGH":
            return .orange
        case "EXTREME":
            return .red
        default:
            return .gray
        }
    }
    
    private var probabilityPercentage: String {
        "\(Int(prediction.prediction.fireProbability * 100))%"
    }
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    
                    // MARK: Risk Header
                    
                    VStack(spacing: 10) {
                        
                        ZStack {
                            Circle()
                                .fill(riskColor.opacity(0.2))
                                .frame(width: 90, height: 90)
                            
                            Text("🔥")
                                .font(.system(size: 40))
                        }
                        
                        Text(
                            prediction.prediction.riskLevel.uppercased()
                        )
                        .font(.largeTitle)
                        .bold()
                        .foregroundStyle(riskColor)
                        
                        Text("Fire Risk")
                            .foregroundStyle(.secondary)
                    }
                    
                    // MARK: Probability
                    
                    VStack(spacing: 8) {
                        Text("Fire Probability")
                            .font(.headline)
                        
                        Text(probabilityPercentage)
                            .font(.system(size: 48, weight: .bold))
                            .foregroundStyle(riskColor)
                        
                        ProgressView(
                            value: prediction.prediction.fireProbability
                        )
                        .tint(riskColor)
                    }
                    .padding()
                    .background(.ultraThinMaterial)
                    .clipShape(
                        RoundedRectangle(cornerRadius: 18)
                    )
                    
                    // MARK: Current Weather
                    
                    VStack(alignment: .leading, spacing: 12) {
                        
                        Text("Current Weather")
                            .font(.title3)
                            .bold()
                        
                        WeatherRow(
                            icon: "🌡️",
                            title: "Temperature",
                            value: String(
                                format: "%.1f °C",
                                prediction.weather.temperature
                            )
                        )
                        
                        WeatherRow(
                            icon: "💧",
                            title: "Humidity",
                            value: String(
                                format: "%.1f %%",
                                prediction.weather.humidity
                            )
                        )
                        
                        WeatherRow(
                            icon: "💨",
                            title: "Wind Speed",
                            value: String(
                                format: "%.1f m/s",
                                prediction.weather.windSpeed
                            )
                        )
                        
                        WeatherRow(
                            icon: "🌧️",
                            title: "Rainfall",
                            value: String(
                                format: "%.1f mm",
                                prediction.weather.rainfall
                            )
                        )
                    }
                    .padding()
                    .background(.ultraThinMaterial)
                    .clipShape(
                        RoundedRectangle(cornerRadius: 18)
                    )
                    
                    // MARK: Historical Weather
                    
                    VStack(alignment: .leading, spacing: 12) {
                        
                        Text("Historical Conditions")
                            .font(.title3)
                            .bold()
                        
                        WeatherRow(
                            icon: "🌡️",
                            title: "3-Day Temperature",
                            value: String(
                                format: "%.1f °C",
                                prediction.historicalWeather.temperature3dMean
                            )
                        )
                        
                        WeatherRow(
                            icon: "🌡️",
                            title: "7-Day Temperature",
                            value: String(
                                format: "%.1f °C",
                                prediction.historicalWeather.temperature7dMean
                            )
                        )
                        
                        WeatherRow(
                            icon: "💨",
                            title: "7-Day Wind",
                            value: String(
                                format: "%.1f m/s",
                                prediction.historicalWeather.wind7dMean
                            )
                        )
                        
                        WeatherRow(
                            icon: "🌧️",
                            title: "7-Day Rainfall",
                            value: String(
                                format: "%.1f mm",
                                prediction.historicalWeather.rainfall7dSum
                            )
                        )
                    }
                    .padding()
                    .background(.ultraThinMaterial)
                    .clipShape(
                        RoundedRectangle(cornerRadius: 18)
                    )
                    
                    // MARK: Location
                    
                    VStack(alignment: .leading, spacing: 8) {
                        
                        Text("Grid Location")
                            .font(.title3)
                            .bold()
                        
                        Text(
                            String(
                                format: "Latitude: %.4f",
                                prediction.location.latitude
                            )
                        )
                        
                        Text(
                            String(
                                format: "Longitude: %.4f",
                                prediction.location.longitude
                            )
                        )
                        
                        Text(
                            String(
                                format: "Model Grid: %.4f, %.4f",
                                prediction.location.gridLat,
                                prediction.location.gridLon
                            )
                        )
                        .foregroundStyle(.secondary)
                    }
                    .frame(
                        maxWidth: .infinity,
                        alignment: .leading
                    )
                    .padding()
                    .background(.ultraThinMaterial)
                    .clipShape(
                        RoundedRectangle(cornerRadius: 18)
                    )
                }
                .padding()
            }
            .navigationTitle("Risk Details")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}


// MARK: - Weather Row

struct WeatherRow: View {
    
    let icon: String
    let title: String
    let value: String
    
    var body: some View {
        HStack {
            
            Text(icon)
                .font(.title3)
            
            Text(title)
            
            Spacer()
            
            Text(value)
                .bold()
        }
    }
}
