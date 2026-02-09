import React from 'react';
import { motion } from 'framer-motion';
import MagneticButton from './MagneticButton';
import { TargetIcon, BriefcaseIcon, BoltIcon, GlobeIcon } from './InfographicIcons';

/**
 * Mission/Why section explaining the accelerator's purpose
 */
const MissionSection = () => {
    return (
        <section id="mission" className="relative py-32 px-6">
            <div className="max-w-5xl mx-auto">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    viewport={{ once: true }}
                    className="text-center mb-16"
                >
                    <h2 className="text-3xl md:text-5xl font-bold mb-4">
                        Why <span className="gradient-text">Ascend?</span>
                    </h2>
                </motion.div>

                {/* Content Grid */}
                <div className="grid md:grid-cols-2 gap-12 items-center">
                    {/* Left - Problem Statement */}
                    <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                    >
                        <h3 className="text-2xl font-bold text-white mb-6">
                            India's best builders deserve a bridge to
                            <span className="gradient-text"> global markets.</span>
                        </h3>
                        <div className="space-y-4 text-slate-400 leading-relaxed">
                            <p>
                                IITs produce world-class talent, but the path from campus to
                                Silicon Valley is broken. Too many founders get stuck—building
                                for the wrong markets, missing the right connections,
                                or simply never starting.
                            </p>
                            <p>
                                We're fixing that. Ascend is the accelerator we wish existed when
                                we were students—direct access to capital, mentors who've done it,
                                and a community that pushes you to think bigger.
                            </p>
                        </div>
                    </motion.div>

                    {/* Right - Value Props */}
                    <motion.div
                        initial={{ opacity: 0, x: 30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        viewport={{ once: true }}
                        className="space-y-4"
                    >
                        {[
                            {
                                IconComponent: TargetIcon,
                                title: 'Curated Community',
                                desc: 'of IITians, by IITians, for IITians',
                            },
                            {
                                IconComponent: BriefcaseIcon,
                                title: 'Silicon Valley Access',
                                desc: 'Week long immersion in SF. Demo Day. VC intros. Office hours.',
                            },
                            {
                                IconComponent: BoltIcon,
                                title: 'Founder-First Terms',
                                desc: 'Minimal Equity, because it should be yours. Cheques Upto 7 Cr',
                            },
                            {
                                IconComponent: GlobeIcon,
                                title: 'Global Network',
                                desc: '200+ alumni across 15 countries. Lifetime access.',
                            },
                        ].map((item, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5, delay: 0.1 * i }}
                                viewport={{ once: true }}
                                className="glass-card p-5 flex gap-4"
                            >
                                <item.IconComponent size={36} />
                                <div>
                                    <h4 className="font-semibold text-white mb-1">{item.title}</h4>
                                    <p className="text-sm text-slate-400">{item.desc}</p>
                                </div>
                            </motion.div>
                        ))}
                    </motion.div>
                </div>

                {/* CTA */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    viewport={{ once: true }}
                    className="text-center mt-16"
                >
                    <MagneticButton
                        href="#tracks"
                        className="px-8 py-3 rounded-full bg-white/5 hover:bg-white/10 
                       text-white font-medium transition-all border border-white/10"
                    >
                        See the Tracks →
                    </MagneticButton>
                </motion.div>
            </div>
        </section>
    );
};

export default MissionSection;
