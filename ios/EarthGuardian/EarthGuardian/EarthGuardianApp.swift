//
//  EarthGuardianApp.swift
//  EarthGuardian
//
//  Created by CU_Student26 on 17/08/26.
//


import SwiftUI

@main
struct EarthGuardianApp: App {

    @State private var showSplash = true

    var body: some Scene {
        WindowGroup {
            ZStack {
                if showSplash {
                    SplashView()
                        .transition(.opacity)
                } else {
                    ContentView()
                        .transition(.opacity)
                }
            }
            .task {
                try? await Task.sleep(for: .seconds(2))

                withAnimation(.easeInOut(duration: 0.5)) {
                    showSplash = false
                }
            }
        }
    }
}

