import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import MagneticButton from './MagneticButton';
import { SoloBuilderIcon, RocketIcon } from './InfographicIcons';

gsap.registerPlugin(ScrollTrigger);

/**
 * Tracks section - HPI vs Startup Track with scroll-triggered reveal
 */
const TracksSection = () => {
    const sectionRef = useRef(null);

    useEffect(() => {
        const tracks = sectionRef.current.querySelectorAll('.track-card');

        ScrollTrigger.create({
            trigger: sectionRef.current,
            start: 'top 70%',
            onEnter: () => {
                gsap.fromTo(
                    tracks,
                    { opacity: 0, y: 60 },
                    {
                        opacity: 1,
                        y: 0,
                        duration: 0.8,
                        stagger: 0.2,
                        ease: 'power3.out',
                    }
                );
            },
        });

        return () => {
            ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
        };
    }, []);

    return (
        <section id="tracks" ref={sectionRef} className="relative py-32 px-6">
            <div className="max-w-7xl mx-auto">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    viewport={{ once: true }}
                    className="text-center mb-20"
                >
                    <h2 className="text-3xl md:text-5xl font-bold mb-4">
                        Choose your path
                    </h2>
                    <p className="text-slate-400">Two tracks. One community.</p>
                </motion.div>

                {/* Track Cards */}
                <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
                    {/* HPI Track */}
                    <div className="track-card opacity-0 rounded-3xl overflow-hidden border-t-4 border-t-z5-pink bg-white/5 backdrop-blur-xl">
                        <div className="p-8 bg-z5-pink/5">
                            <div className="mb-4"><SoloBuilderIcon size={48} /></div>
                            <h3 className="text-2xl font-bold text-white mb-2">
                                Building solo?
                            </h3>
                            <p className="text-slate-400 text-sm">Let's find your co-founder.</p>
                        </div>

                        <div className="p-8 space-y-6">
                            <div>
                                <div className="text-4xl font-bold gradient-text">$5,000</div>
                                <p className="text-sm text-slate-500">
                                    Non-dilutive grant + matching support
                                </p>
                            </div>

                            <div className="space-y-3 text-sm text-slate-400">
                                <p>✓ Technical expert or domain specialist</p>
                                <p>✓ Curious, Sharp and insanely impatient</p>
                                <p>✓ Ready to find your co-founder</p>
                                <p>✓ Ready to build</p>
                            </div>
                        </div>

                        <div className="p-8 border-t border-white/5">
                            <MagneticButton
                                href="#apply"
                                className="block w-full py-3 text-center rounded-xl bg-z5-pink/10 hover:bg-z5-pink/20 
                         text-z5-pink font-semibold transition-all border border-z5-pink/20"
                            >
                                Apply as Individual
                            </MagneticButton>
                        </div>
                    </div>

                    {/* Startup Track */}
                    <div className="track-card opacity-0 rounded-3xl overflow-hidden border-t-4 border-t-z5-purple bg-white/5 backdrop-blur-xl">
                        <div className="p-8 bg-z5-purple/5">
                            <div className="mb-4"><RocketIcon size={48} /></div>
                            <h3 className="text-2xl font-bold text-white mb-2">
                                Already have a team?
                            </h3>
                            <p className="text-slate-400 text-sm">Let's get you funded.</p>
                        </div>

                        <div className="p-8 space-y-6">
                            <div>
                                <div className="text-4xl font-bold gradient-text">$40,000</div>
                                <p className="text-sm text-slate-500">Investment for 4% equity</p>
                            </div>

                            <div className="space-y-3 text-sm text-slate-400">
                                <p>✓ Atleast 1 Founder from an IIT</p>
                                <p>✓ Idea on paper, MVP or working prototype</p>
                                <p>✓ B2B/Enterprise focus</p>
                                <p>✓ Ready to build, fail and scale fast</p>
                            </div>
                        </div>

                        <div className="p-8 border-t border-white/5">
                            <MagneticButton
                                href="#apply"
                                className="block w-full py-3 text-center rounded-xl bg-z5-purple/10 hover:bg-z5-purple/20 
                         text-z5-purple font-semibold transition-all border border-z5-purple/20"
                            >
                                Apply as Startup
                            </MagneticButton>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default TracksSection;
