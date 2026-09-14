//
//  GridRiskSummaryView.swift
//  EarthGuardian
//
//  Created by CU_Student26 on 02/09/26.
//

import SwiftUI

struct GridRiskSummaryView: View {
    
    let predictions: [GridPrediction]
    
    private var averageProbability: Double {
        guard !predictions.isEmpty else {
            return 0
        }
        
        return predictions
            .map { $0.prediction.fireProbability }
            .reduce(0, +) / Double(predictions.count)
    }
    
    private var highestProbability: Double {
        predictions
            .map { $0.prediction.fireProbability }
            .max() ?? 0
    }
    
    private var highRiskCount: Int {
        predictions.filter {
            let risk = $0.prediction.riskLevel.uppercased()
            return risk == "HIGH" || risk == "EXTREME"
        }.count
    }
    
    var body: some View {
        
        VStack(alignment: .leading, spacing: 15) {
            
            Text("Regional Risk Analysis")
                .font(.title3)
                .bold()
            
            HStack(spacing: 10) {
                
                RiskStatistic(
                    title: "Average",
                    value: "\(Int(averageProbability * 100))%"
                )
                
                RiskStatistic(
                    title: "Highest",
                    value: "\(Int(highestProbability * 100))%"
                )
                
                RiskStatistic(
                    title: "High Risk",
                    value: "\(highRiskCount)"
                )
            }
        }
        .padding()
        .background(.ultraThinMaterial)
        .clipShape(
            RoundedRectangle(cornerRadius: 18)
        )
    }
}


struct RiskStatistic: View {
    
    let title: String
    let value: String
    
    var body: some View {
        VStack(spacing: 5) {
            
            Text(value)
                .font(.title2)
                .bold()
            
            Text(title)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
    }
}
