import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MagneticButton from './MagneticButton';

/**
 * Glassmorphic navigation bar with breathing logo animation
 */
const Navigation = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const navLinks = [
        { href: '#mission', label: 'Mission' },
        { href: '#tracks', label: 'Tracks' },
        { href: '#journey', label: 'Journey' },
        { href: '#community', label: 'Community' },
    ];

    return (
        <nav className="fixed w-full z-50 bg-z5-dark/80 backdrop-blur-xl border-b border-white/5">
            <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
                {/* Logo with breathing glow */}
                <motion.a
                    href="#"
                    className="flex items-center gap-3"
                    whileHover={{ scale: 1.02 }}
                >
                    <div className="relative">
                        <img
                            src="/ascend-logo.png"
                            alt="Z5 Ascend"
                            className="h-10 w-auto animate-breathe"
                        />
                    </div>
                </motion.a>

                {/* Desktop Navigation */}
                <div className="hidden md:flex items-center gap-8">
                    {navLinks.map((link) => (
                        <motion.a
                            key={link.href}
                            href={link.href}
                            className="text-sm font-medium text-slate-400 hover:text-white transition-colors relative"
                            whileHover={{ y: -2 }}
                        >
                            {link.label}
                        </motion.a>
                    ))}

                    <MagneticButton
                        href="#apply"
                        className="px-6 py-2.5 rounded-full bg-white/5 hover:bg-white/10 
                       text-white text-sm font-medium transition-all 
                       border border-white/10 hover:border-white/20"
                    >
                        Apply Now
                    </MagneticButton>
                </div>

                {/* Mobile Menu Button */}
                <button
                    onClick={() => setIsMenuOpen(!isMenuOpen)}
                    className="md:hidden p-2 text-white"
                    aria-label="Toggle menu"
                >
                    <svg
                        className="w-6 h-6"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        {isMenuOpen ? (
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M6 18L18 6M6 6l12 12"
                            />
                        ) : (
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M4 6h16M4 12h16M4 18h16"
                            />
                        )}
                    </svg>
                </button>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {isMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="md:hidden bg-z5-dark/95 backdrop-blur-xl border-t border-white/5"
                    >
                        <div className="px-6 py-4 space-y-4">
                            {navLinks.map((link) => (
                                <a
                                    key={link.href}
                                    href={link.href}
                                    className="block text-slate-400 hover:text-white transition-colors py-2"
                                    onClick={() => setIsMenuOpen(false)}
                                >
                                    {link.label}
                                </a>
                            ))}
                            <a
                                href="#apply"
                                className="block w-full py-3 text-center rounded-full bg-gradient-to-r from-z5-purple to-z5-pink text-white font-semibold"
                                onClick={() => setIsMenuOpen(false)}
                            >
                                Apply Now
                            </a>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
};

export default Navigation;
