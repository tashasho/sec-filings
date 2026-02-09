import React, { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

/**
 * Scroll-reactive Golden Gate Bridge background.
 * Bridge & skyline use OUTLINE strokes for depth.
 * Waves use gradients. Skyline is more transparent.
 */
const ScrollBackground = () => {
    const { scrollYProgress } = useScroll();

    // Parallax speeds
    const y1 = useTransform(scrollYProgress, [0, 1], ['0%', '-25%']);
    const y2 = useTransform(scrollYProgress, [0, 1], ['0%', '-40%']);
    const y3 = useTransform(scrollYProgress, [0, 1], ['0%', '-20%']);
    const y4 = useTransform(scrollYProgress, [0, 1], ['0%', '-18%']);

    // Opacity: strongest in hero, fades deeper into content
    const opBridge = useTransform(scrollYProgress, [0, 0.15, 0.35, 0.6, 1], [0.18, 0.25, 0.14, 0.07, 0.03]);
    const opSkyline = useTransform(scrollYProgress, [0, 0.15, 0.35, 0.6, 1], [0.05, 0.08, 0.05, 0.03, 0.01]);
    const opWater = useTransform(scrollYProgress, [0, 0.15, 0.35, 0.6, 1], [0.14, 0.2, 0.15, 0.12, 0.12]);
    const opMountains = useTransform(scrollYProgress, [0, 0.15, 0.35, 0.6, 1], [0.06, 0.1, 0.05, 0.03, 0.01]);

    return (
        <div
            className="fixed inset-0 w-full h-full pointer-events-none overflow-hidden"
            style={{ zIndex: 1 }}
            aria-hidden="true"
        >
            {/* ── Layer 1: Distant hills / Marin Headlands (slowest) ── */}
            <motion.div
                className="absolute inset-0 w-full h-full"
                style={{ y: y4, opacity: opMountains }}
            >
                <svg
                    className="absolute bottom-0 w-full"
                    viewBox="0 0 1440 600"
                    preserveAspectRatio="none"
                    style={{ height: '120%' }}
                >
                    <defs>
                        <linearGradient id="hillsOutline" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#6D28D9" />
                            <stop offset="50%" stopColor="#8B5CF6" />
                            <stop offset="100%" stopColor="#6D28D9" />
                        </linearGradient>
                    </defs>
                    {/* Outlined hills - lighter stroke for depth */}
                    <path
                        d="M0,400 C80,340 180,300 300,330 C420,360 500,280 620,260 
                           C740,240 820,300 900,280 C980,260 1060,220 1160,250 
                           C1260,280 1340,320 1440,300"
                        stroke="url(#hillsOutline)"
                        strokeWidth="2"
                        fill="none"
                    />
                    {/* Subtle fill beneath */}
                    <path
                        d="M0,400 C80,340 180,300 300,330 C420,360 500,280 620,260 
                           C740,240 820,300 900,280 C980,260 1060,220 1160,250 
                           C1260,280 1340,320 1440,300 L1440,600 L0,600 Z"
                        fill="url(#hillsOutline)"
                        fillOpacity="0.15"
                    />
                </svg>
            </motion.div>

            {/* ── Layer 2: City skyline — MORE TRANSPARENT, outline only ── */}
            <motion.div
                className="absolute inset-0 w-full h-full"
                style={{ y: y2, opacity: opSkyline }}
            >
                <svg
                    className="absolute bottom-0 w-full"
                    viewBox="0 0 1440 600"
                    preserveAspectRatio="none"
                    style={{ height: '110%' }}
                >
                    <defs>
                        <linearGradient id="cityOutline" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#8B5CF6" stopOpacity="0.6" />
                            <stop offset="50%" stopColor="#A855F7" stopOpacity="0.4" />
                            <stop offset="100%" stopColor="#EC4899" stopOpacity="0.6" />
                        </linearGradient>
                    </defs>
                    {/* Outlined skyline — stroke only, no fill */}
                    <path
                        d="M0,500 
                           L60,500 L60,440 L80,440 L80,460 L100,460 L100,420 L115,420 L115,400 L130,400 L130,440 
                           L160,440 L160,470 L200,470 L200,430 L220,430 L220,390 L235,390 L235,420 L260,420 
                           L260,460 L300,460 L300,480 L340,480 L340,450 L360,450 L360,410 L375,410 L375,440 
                           L400,440 L400,470 L440,470 L440,500 
                           L500,500 L500,480 L520,480 L520,450 L540,450 L540,420 L555,420 L555,440 L580,440 
                           L580,470 L620,470 L620,490 L660,490 L660,460 L680,460 L680,430 L700,430
                           L700,460 L740,460 L740,490 
                           L800,490 L800,500 
                           L860,500 L860,470 L880,470 L880,440 L900,440 L900,410 L915,410 L915,380 L930,380 
                           L930,420 L960,420 L960,450 L1000,450 L1000,480 
                           L1040,480 L1040,460 L1060,460 L1060,430 L1080,430 L1080,400 L1095,400 L1095,430
                           L1120,430 L1120,460 L1160,460 L1160,490 
                           L1200,490 L1200,470 L1220,470 L1220,440 L1240,440 L1240,410 L1260,410 L1260,440
                           L1300,440 L1300,470 L1340,470 L1340,490 L1380,490 L1380,500 L1440,500"
                        stroke="url(#cityOutline)"
                        strokeWidth="1.5"
                        fill="none"
                    />
                    {/* Tiny window dots for depth */}
                    {[115, 225, 360, 540, 680, 915, 1080, 1245].map((x, i) => (
                        <g key={`w${i}`}>
                            <rect x={x} y={420 + (i % 3) * 15} width="3" height="3" fill="#A855F7" fillOpacity="0.3" />
                            <rect x={x + 8} y={425 + (i % 2) * 10} width="3" height="3" fill="#8B5CF6" fillOpacity="0.25" />
                        </g>
                    ))}
                </svg>
            </motion.div>

            {/* ── Layer 3: Golden Gate Bridge — OUTLINED with lighter stroke for depth ── */}
            <motion.div
                className="absolute inset-0 w-full h-full"
                style={{ y: y1, opacity: opBridge }}
            >
                <svg
                    className="absolute bottom-0 w-full"
                    viewBox="0 0 1440 700"
                    preserveAspectRatio="none"
                    style={{ height: '130%' }}
                >
                    <defs>
                        {/* Main structural gradient — pink to purple */}
                        <linearGradient id="bridgeStroke" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stopColor="#F472B6" />
                            <stop offset="40%" stopColor="#EC4899" />
                            <stop offset="100%" stopColor="#A855F7" />
                        </linearGradient>
                        {/* Lighter outline for depth/glow */}
                        <linearGradient id="bridgeGlow" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stopColor="#F9A8D4" stopOpacity="0.5" />
                            <stop offset="100%" stopColor="#C4B5FD" stopOpacity="0.3" />
                        </linearGradient>
                        {/* Cable gradient */}
                        <linearGradient id="cableStroke" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#F472B6" />
                            <stop offset="50%" stopColor="#C084FC" />
                            <stop offset="100%" stopColor="#F472B6" />
                        </linearGradient>
                        <linearGradient id="cableGlow" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#FBCFE8" stopOpacity="0.3" />
                            <stop offset="50%" stopColor="#DDD6FE" stopOpacity="0.2" />
                            <stop offset="100%" stopColor="#FBCFE8" stopOpacity="0.3" />
                        </linearGradient>
                        {/* Deck gradient */}
                        <linearGradient id="deckStroke" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#A855F7" />
                            <stop offset="50%" stopColor="#EC4899" />
                            <stop offset="100%" stopColor="#A855F7" />
                        </linearGradient>
                    </defs>

                    {/* ── Road deck — outlined ── */}
                    {/* Glow layer (lighter, wider) */}
                    <line x1="60" y1="525" x2="1380" y2="525" stroke="url(#cableGlow)" strokeWidth="14" />
                    {/* Main deck outline */}
                    <rect x="60" y="520" width="1320" height="10" rx="2" stroke="url(#deckStroke)" strokeWidth="2" fill="none" />

                    {/* ── Left Tower — outlined with glow ── */}
                    <g>
                        {/* Glow (lighter outer outline) */}
                        <rect x="377" y="272" width="50" height="260" rx="3" stroke="url(#bridgeGlow)" strokeWidth="6" fill="none" />
                        {/* Left column outline */}
                        <rect x="380" y="280" width="14" height="255" rx="1" stroke="url(#bridgeStroke)" strokeWidth="2" fill="none" />
                        {/* Right column outline */}
                        <rect x="410" y="280" width="14" height="255" rx="1" stroke="url(#bridgeStroke)" strokeWidth="2" fill="none" />
                        {/* Tower cap */}
                        <rect x="375" y="275" width="54" height="10" rx="2" stroke="url(#bridgeStroke)" strokeWidth="2" fill="none" />
                        {/* Cross braces */}
                        {[320, 370, 420, 470].map((braceY, i) => (
                            <line key={`lb${i}`} x1="394" y1={braceY} x2="410" y2={braceY} stroke="url(#bridgeStroke)" strokeWidth="1.5" />
                        ))}
                    </g>

                    {/* ── Right Tower — outlined with glow ── */}
                    <g>
                        <rect x="1017" y="272" width="50" height="260" rx="3" stroke="url(#bridgeGlow)" strokeWidth="6" fill="none" />
                        <rect x="1020" y="280" width="14" height="255" rx="1" stroke="url(#bridgeStroke)" strokeWidth="2" fill="none" />
                        <rect x="1050" y="280" width="14" height="255" rx="1" stroke="url(#bridgeStroke)" strokeWidth="2" fill="none" />
                        <rect x="1015" y="275" width="54" height="10" rx="2" stroke="url(#bridgeStroke)" strokeWidth="2" fill="none" />
                        {[320, 370, 420, 470].map((braceY, i) => (
                            <line key={`rb${i}`} x1="1034" y1={braceY} x2="1050" y2={braceY} stroke="url(#bridgeStroke)" strokeWidth="1.5" />
                        ))}
                    </g>

                    {/* ── Main suspension cables — with glow outline ── */}
                    {/* Glow layer (lighter, wider) */}
                    <path d="M60,380 Q220,520 402,280" stroke="url(#cableGlow)" strokeWidth="8" fill="none" />
                    <path d="M402,280 Q720,520 1042,280" stroke="url(#cableGlow)" strokeWidth="8" fill="none" />
                    <path d="M1042,280 Q1240,520 1380,380" stroke="url(#cableGlow)" strokeWidth="8" fill="none" />
                    {/* Main cable strokes */}
                    <path d="M60,380 Q220,520 402,280" stroke="url(#cableStroke)" strokeWidth="3" fill="none" />
                    <path d="M402,280 Q720,520 1042,280" stroke="url(#cableStroke)" strokeWidth="3" fill="none" />
                    <path d="M1042,280 Q1240,520 1380,380" stroke="url(#cableStroke)" strokeWidth="3" fill="none" />

                    {/* ── Vertical suspender cables ── */}
                    {/* Left approach */}
                    {[120, 170, 220, 270, 320].map((x, i) => {
                        const t = (x - 60) / (402 - 60);
                        const cy = 380 + (520 - 380) * 2 * t * (1 - t) + (280 - 380) * t * t;
                        const topY = Math.min(cy, 518);
                        return <line key={`la${i}`} x1={x} y1={topY} x2={x} y2={520} stroke="#C084FC" strokeWidth="1" strokeOpacity="0.6" />;
                    })}
                    {/* Main span */}
                    {[460, 510, 560, 610, 660, 720, 780, 840, 890, 940, 990].map((x, i) => {
                        const t = (x - 402) / (1042 - 402);
                        const cy = 280 + (520 - 280) * 4 * t * (1 - t);
                        const topY = Math.min(cy, 518);
                        return <line key={`ms${i}`} x1={x} y1={topY} x2={x} y2={520} stroke="#C084FC" strokeWidth="1" strokeOpacity="0.6" />;
                    })}
                    {/* Right approach */}
                    {[1100, 1150, 1200, 1250, 1320].map((x, i) => {
                        const t = (x - 1042) / (1380 - 1042);
                        const cy = 280 + (520 - 280) * 2 * t * (1 - t) + (380 - 280) * t * t;
                        const topY = Math.min(cy, 518);
                        return <line key={`ra${i}`} x1={x} y1={topY} x2={x} y2={520} stroke="#C084FC" strokeWidth="1" strokeOpacity="0.6" />;
                    })}
                </svg>
            </motion.div>

            {/* ── Layer 4: Water surface — GRADIENT waves ── */}
            <motion.div
                className="absolute inset-0 w-full h-full"
                style={{ y: y3, opacity: opWater }}
            >
                <svg
                    className="absolute bottom-0 w-full"
                    viewBox="0 0 1440 300"
                    preserveAspectRatio="none"
                    style={{ height: '60%' }}
                >
                    <defs>
                        {/* Multi-stop gradient for waves */}
                        <linearGradient id="waveGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#8B5CF6" stopOpacity="0.5" />
                            <stop offset="30%" stopColor="#7C3AED" stopOpacity="0.3" />
                            <stop offset="60%" stopColor="#EC4899" stopOpacity="0.4" />
                            <stop offset="100%" stopColor="#8B5CF6" stopOpacity="0.5" />
                        </linearGradient>
                        <linearGradient id="waveGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#6D28D9" stopOpacity="0.4" />
                            <stop offset="50%" stopColor="#A855F7" stopOpacity="0.25" />
                            <stop offset="100%" stopColor="#DB2777" stopOpacity="0.4" />
                        </linearGradient>
                        <linearGradient id="waveGrad3" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#7C3AED" stopOpacity="0.25" />
                            <stop offset="40%" stopColor="#EC4899" stopOpacity="0.15" />
                            <stop offset="80%" stopColor="#8B5CF6" stopOpacity="0.2" />
                            <stop offset="100%" stopColor="#6D28D9" stopOpacity="0.25" />
                        </linearGradient>
                        {/* Wave outline glow */}
                        <linearGradient id="waveOutline" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#C4B5FD" stopOpacity="0.5" />
                            <stop offset="50%" stopColor="#F9A8D4" stopOpacity="0.4" />
                            <stop offset="100%" stopColor="#C4B5FD" stopOpacity="0.5" />
                        </linearGradient>
                    </defs>
                    {/* Wave 1 — with gradient fill + light outline */}
                    <path
                        d="M0,120 C120,95 240,145 360,110 C480,80 600,135 720,105 
                           C840,80 960,130 1080,100 C1200,75 1320,125 1440,95"
                        stroke="url(#waveOutline)"
                        strokeWidth="2"
                        fill="none"
                    />
                    <path
                        d="M0,120 C120,95 240,145 360,110 C480,80 600,135 720,105 
                           C840,80 960,130 1080,100 C1200,75 1320,125 1440,95 
                           L1440,300 L0,300 Z"
                        fill="url(#waveGrad1)"
                    />
                    {/* Wave 2 */}
                    <path
                        d="M0,160 C100,142 220,178 340,152 C460,130 580,168 700,148 
                           C820,130 940,162 1060,142 C1180,125 1300,160 1440,138"
                        stroke="url(#waveOutline)"
                        strokeWidth="1.5"
                        fill="none"
                    />
                    <path
                        d="M0,160 C100,142 220,178 340,152 C460,130 580,168 700,148 
                           C820,130 940,162 1060,142 C1180,125 1300,160 1440,138 
                           L1440,300 L0,300 Z"
                        fill="url(#waveGrad2)"
                    />
                    {/* Wave 3 */}
                    <path
                        d="M0,200 C140,188 280,212 420,195 C560,178 700,208 840,192 
                           C980,176 1120,202 1260,188 C1380,178 1440,195 1440,195 
                           L1440,300 L0,300 Z"
                        fill="url(#waveGrad3)"
                    />
                </svg>
            </motion.div>

            {/* ── Ambient glow spots ── */}
            <motion.div
                className="absolute top-[25%] left-[20%] w-[500px] h-[500px] rounded-full"
                style={{
                    background: 'radial-gradient(circle, rgba(139,92,246,0.08) 0%, transparent 70%)',
                    y: y2,
                }}
            />
            <motion.div
                className="absolute top-[55%] right-[15%] w-[500px] h-[500px] rounded-full"
                style={{
                    background: 'radial-gradient(circle, rgba(236,72,153,0.06) 0%, transparent 70%)',
                    y: y1,
                }}
            />
        </div>
    );
};

export default ScrollBackground;
