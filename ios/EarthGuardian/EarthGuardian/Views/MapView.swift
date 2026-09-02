import SwiftUI
import MapKit
import CoreLocation

struct MapView: View {
    
    let location: CLLocation
    let gridPredictions: [GridPrediction]
    
    @State private var position: MapCameraPosition
    
    init(
        location: CLLocation,
        gridPredictions: [GridPrediction] = []
    ) {
        self.location = location
        self.gridPredictions = gridPredictions
        
        let region = MKCoordinateRegion(
            center: location.coordinate,
            latitudinalMeters: 100000,
            longitudinalMeters: 100000
        )
        
        _position = State(initialValue: .region(region))
    }
    
    var body: some View {
        ZStack(alignment: .topLeading) {
            
            Map(position: $position) {
                
                // MARK: User Location
                
                Annotation(
                    "You",
                    coordinate: location.coordinate
                ) {
                    ZStack {
                        Circle()
                            .fill(.blue)
                            .frame(width: 24, height: 24)
                        
                        Circle()
                            .stroke(.white, lineWidth: 3)
                            .frame(width: 24, height: 24)
                    }
                }
                
                // MARK: Risk Grid
                
                ForEach(gridPredictions) { prediction in
                    
                    Annotation(
                        prediction.prediction.riskLevel,
                        coordinate: CLLocationCoordinate2D(
                            latitude: prediction.location.latitude,
                            longitude: prediction.location.longitude
                        )
                    ) {
                        RiskMapMarker(
                            riskLevel: prediction.prediction.riskLevel,
                            probability: prediction.prediction.fireProbability
                        )
                    }
                }
            }
            .clipShape(
                RoundedRectangle(cornerRadius: 20)
            )
            
            // MARK: Legend
            
            RiskLegend()
                .padding(12)
        }
    }
}


// MARK: - Risk Map Marker

struct RiskMapMarker: View {
    
    let riskLevel: String
    let probability: Double
    
    var markerColor: Color {
        switch riskLevel.uppercased() {
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
    
    var body: some View {
        ZStack {
            
            // Risk area
            Circle()
                .fill(markerColor.opacity(0.25))
                .frame(width: 50, height: 50)
            
            // Main marker
            Circle()
                .fill(markerColor.opacity(0.9))
                .frame(width: 28, height: 28)
            
            Circle()
                .stroke(.white, lineWidth: 2)
                .frame(width: 28, height: 28)
            
            Circle()
                .fill(.white)
                .frame(width: 7, height: 7)
        }
    }
}


// MARK: - Risk Legend

struct RiskLegend: View {
    
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            
            Text("🔥 Fire Risk")
                .font(.headline)
            
            RiskLegendRow(
                color: .green,
                text: "Low"
            )
            
            RiskLegendRow(
                color: .yellow,
                text: "Moderate"
            )
            
            RiskLegendRow(
                color: .orange,
                text: "High"
            )
            
            RiskLegendRow(
                color: .red,
                text: "Extreme"
            )
        }
        .padding(12)
        .background(.ultraThinMaterial)
        .clipShape(
            RoundedRectangle(cornerRadius: 14)
        )
    }
}


struct RiskLegendRow: View {
    
    let color: Color
    let text: String
    
    var body: some View {
        HStack(spacing: 8) {
            
            Circle()
                .fill(color)
                .frame(width: 10, height: 10)
            
            Text(text)
                .font(.caption)
        }
    }
}
