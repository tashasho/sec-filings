import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import MagneticButton from './MagneticButton';

/**
 * Hero section with typewriter effect looping through taglines
 */
const HeroSection = () => {
    const [displayText, setDisplayText] = useState('');
    const [phraseIndex, setPhraseIndex] = useState(0);
    const [isTyping, setIsTyping] = useState(true);

    const phrases = [
        'With people who get it.',
        'From Idea to Enterprise.',
        'Beyond boundaries.',
    ];

    const typeText = useCallback(() => {
        const currentPhrase = phrases[phraseIndex];

        if (isTyping) {
            if (displayText.length < currentPhrase.length) {
                setTimeout(() => {
                    setDisplayText(currentPhrase.substring(0, displayText.length + 1));
                }, 80);
            } else {
                // Pause before erasing
                setTimeout(() => setIsTyping(false), 2000);
            }
        } else {
            if (displayText.length > 0) {
                setTimeout(() => {
                    setDisplayText(displayText.substring(0, displayText.length - 1));
                }, 40);
            } else {
                // Move to next phrase
                setPhraseIndex((prev) => (prev + 1) % phrases.length);
                setIsTyping(true);
            }
        }
    }, [displayText, phraseIndex, isTyping, phrases]);

    useEffect(() => {
        typeText();
    }, [typeText]);

    return (
        <section className="relative min-h-screen flex items-center justify-center px-6 pt-20">
            <div className="max-w-4xl mx-auto text-center z-10">
                {/* Status Badge */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-xs font-medium mb-12"
                >
                    <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                    Applications Open · Fall 2025
                </motion.div>

                {/* Headline */}
                <motion.h1
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className="text-5xl md:text-7xl font-bold mb-8 leading-tight"
                >
                    Build what matters.
                    <br />
                    <span className="gradient-text">
                        {displayText}
                        <span className="animate-pulse text-z5-purple">|</span>
                    </span>
                </motion.h1>

                {/* Subtext */}
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-12 leading-relaxed"
                >
                    A 4-week accelerator connecting India's brightest builders with Silicon
                    Valley's ecosystem. <span className="text-white font-medium">For dreamers, builders and world changers.</span>
                </motion.p>

                {/* CTA Buttons */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.6 }}
                    className="flex flex-col items-center gap-4"
                >
                    <MagneticButton
                        href="#apply"
                        className="px-10 py-4 rounded-full gradient-button text-lg"
                    >
                        Start Your Journey →
                    </MagneticButton>

                    <motion.a
                        href="#mission"
                        className="text-sm text-slate-500 hover:text-slate-300 transition-colors"
                        whileHover={{ y: 3 }}
                        transition={{ type: 'spring', stiffness: 400 }}
                    >
                        Learn how it works ↓
                    </motion.a>
                </motion.div>
            </div>

            {/* Gradient Orbs for depth */}
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-z5-purple/10 rounded-full blur-3xl pointer-events-none" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-z5-pink/10 rounded-full blur-3xl pointer-events-none" />
        </section>
    );
};

export default HeroSection;
