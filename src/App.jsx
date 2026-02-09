import React from 'react';
import { useCustomCursor } from './hooks';
import {
    ParticleBackground,
    ScrollBackground,
    Navigation,
    HeroSection,
    MissionSection,
    CommunitySection,
    TracksSection,
    JourneySection,
    ApplySection,
} from './components';

/**
 * Z5 Ascend Accelerator Website
 * A quiet sanctuary for ambitious builders - dark, sophisticated, alive with subtle organic motion
 */
const App = () => {
    // Initialize custom cursor on desktop
    useCustomCursor();

    return (
        <div className="bg-z5-dark text-white min-h-screen overflow-x-hidden">
            {/* Three.js Particle Background */}
            <ParticleBackground />

            {/* Scroll-reactive layered SVG background */}
            <ScrollBackground />

            {/* Navigation */}
            <Navigation />

            {/* Main Content */}
            <main className="relative z-10">
                <HeroSection />
                <MissionSection />
                <CommunitySection />
                <TracksSection />
                <JourneySection />
                <ApplySection />
            </main>

            {/* Footer */}
            <footer className="relative z-10 py-16 border-t border-white/5">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                        {/* Logo */}
                        <div className="flex items-center gap-3">
                            <img
                                src="/ascend-logo.png"
                                alt="Z5 Ascend"
                                className="h-8 w-auto opacity-60"
                            />
                        </div>

                        {/* Links */}
                        <div className="flex items-center gap-6 text-sm text-slate-500">
                            <a href="#" className="hover:text-white transition-colors">
                                Privacy
                            </a>
                            <a href="#" className="hover:text-white transition-colors">
                                Terms
                            </a>
                            <a
                                href="mailto:hello@z5capital.com"
                                className="hover:text-white transition-colors"
                            >
                                Contact
                            </a>
                        </div>

                        {/* Copyright */}
                        <p className="text-xs text-slate-600 text-center md:text-right">
                            © 2025 Z5 Capital. Building bridges between India and Silicon Valley.
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default App;
