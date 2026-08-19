//
//  Prediction.swift
//  EarthGuardian
//
//  Created by CU_Student26 on 17/08/26.
//
import Foundation

struct LocationInfo: Codable {
    let latitude: Double
    let longitude: Double
    let gridLat: Double
    let gridLon: Double
    
    enum CodingKeys: String, CodingKey {
        case latitude
        case longitude
        case gridLat = "grid_lat"
        case gridLon = "grid_lon"
    }
}

struct WeatherInfo: Codable {
    let temperature: Double
    let humidity: Double
    let windSpeed: Double
    let rainfall: Double
    
    enum CodingKeys: String, CodingKey {
        case temperature
        case humidity
        case windSpeed = "wind_speed"
        case rainfall
    }
}

struct HistoricalWeather: Codable {
    let temperature3dMean: Double
    let temperature7dMean: Double
    let humidity3dMean: Double
    let humidity7dMean: Double
    let wind3dMean: Double
    let wind7dMean: Double
    let rainfall3dSum: Double
    let rainfall7dSum: Double
    
    enum CodingKeys: String, CodingKey {
        case temperature3dMean = "temperature_3d_mean"
        case temperature7dMean = "temperature_7d_mean"
        case humidity3dMean = "humidity_3d_mean"
        case humidity7dMean = "humidity_7d_mean"
        case wind3dMean = "wind_3d_mean"
        case wind7dMean = "wind_7d_mean"
        case rainfall3dSum = "rainfall_3d_sum"
        case rainfall7dSum = "rainfall_7d_sum"
    }
}

struct PredictionInfo: Codable {
    let fireProbability: Double
    let firePrediction: Int
    let riskLevel: String
    let threshold: Double
    
    enum CodingKeys: String, CodingKey {
        case fireProbability = "fire_probability"
        case firePrediction = "fire_prediction"
        case riskLevel = "risk_level"
        case threshold
    }
}

struct PredictionResponse: Codable {
    let location: LocationInfo
    let weather: WeatherInfo
    let historicalWeather: HistoricalWeather
    let prediction: PredictionInfo
    
    enum CodingKeys: String, CodingKey {
        case location
        case weather
        case historicalWeather = "historical_weather"
        case prediction
    }
}
struct GridPredictionResponse: Codable {

    let center: GridCenter
    let radius: Double
    let points: Int
    let count: Int
    let results: [GridPrediction]
}


struct GridCenter: Codable {

    let latitude: Double
    let longitude: Double
}


struct GridPrediction: Codable, Identifiable {

    var id: String {
        "\(latitude)-\(longitude)"
    }

    let latitude: Double
    let longitude: Double

    let gridLat: Double?
    let gridLon: Double?

    let fireProbability: Double
    let firePrediction: Int
    let riskLevel: String
    let threshold: Double

    enum CodingKeys: String, CodingKey {

        case latitude
        case longitude

        case gridLat = "grid_lat"
        case gridLon = "grid_lon"

        case fireProbability = "fire_probability"
        case firePrediction = "fire_prediction"
        case riskLevel = "risk_level"
        case threshold
    }
}
