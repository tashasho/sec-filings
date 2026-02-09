import React from 'react';

/**
 * Outlined infographic-style SVG icons.
 * All icons use stroke-only rendering with gradient for depth,
 * matching the bridge outline aesthetic.
 */

const iconStyle = {
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
    fill: 'none',
};

// Gradient definition reusable across icons
const IconGradient = ({ id = 'iconGrad' }) => (
    <defs>
        <linearGradient id={id} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#EC4899" />
            <stop offset="100%" stopColor="#8B5CF6" />
        </linearGradient>
    </defs>
);

const IconWrapper = ({ children, size = 40, className = '' }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        className={className}
        style={iconStyle}
    >
        <IconGradient />
        {children}
    </svg>
);

// ── Target / Crosshair — Curated Community ──
export const TargetIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        <circle cx="12" cy="12" r="10" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="6" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="2" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="12" y1="2" x2="12" y2="5" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="12" y1="19" x2="12" y2="22" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="2" y1="12" x2="5" y2="12" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="19" y1="12" x2="22" y2="12" stroke="url(#iconGrad)" strokeWidth="1.5" />
    </IconWrapper>
);

// ── Briefcase — Silicon Valley Access ──
export const BriefcaseIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        <rect x="2" y="7" width="20" height="14" rx="2" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="2" y1="13" x2="22" y2="13" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <circle cx="12" cy="13" r="1.5" stroke="url(#iconGrad)" strokeWidth="1" />
    </IconWrapper>
);

// ── Lightning Bolt — Founder-First Terms ──
export const BoltIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        <path d="M13 2L4.5 12.5h6l-1 9.5L19 11.5h-6l1-9.5z" stroke="url(#iconGrad)" strokeWidth="1.5" />
    </IconWrapper>
);

// ── Globe — Global Network ──
export const GlobeIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        <circle cx="12" cy="12" r="10" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <ellipse cx="12" cy="12" rx="4" ry="10" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="2" y1="12" x2="22" y2="12" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <path d="M4 7h16" stroke="url(#iconGrad)" strokeWidth="1" strokeDasharray="2 2" />
        <path d="M4 17h16" stroke="url(#iconGrad)" strokeWidth="1" strokeDasharray="2 2" />
    </IconWrapper>
);

// ── Solo Builder / Astronaut — HPI Track ──
export const SoloBuilderIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        <circle cx="12" cy="8" r="5" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <path d="M12 3v-1M9 4.5L8 3M15 4.5l1-1.5" stroke="url(#iconGrad)" strokeWidth="1.2" />
        <path d="M5 21v-2a7 7 0 0114 0v2" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <circle cx="10.5" cy="7.5" r="0.8" stroke="url(#iconGrad)" strokeWidth="1" />
        <circle cx="13.5" cy="7.5" r="0.8" stroke="url(#iconGrad)" strokeWidth="1" />
    </IconWrapper>
);

// ── Rocket — Startup Track ──
export const RocketIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        <path d="M12 2C12 2 7 6 7 12c0 3 1.5 5 2.5 6.5L12 22l2.5-3.5C15.5 17 17 15 17 12c0-6-5-10-5-10z" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <circle cx="12" cy="11" r="2" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <path d="M7 12H4l1.5-3" stroke="url(#iconGrad)" strokeWidth="1.2" />
        <path d="M17 12h3l-1.5-3" stroke="url(#iconGrad)" strokeWidth="1.2" />
    </IconWrapper>
);

// ── Compass/Foundation — Week 1 ──
export const CompassIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        <circle cx="12" cy="12" r="10" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <polygon points="12,4 14,10 12,8 10,10" stroke="url(#iconGrad)" strokeWidth="1.2" />
        <polygon points="12,20 10,14 12,16 14,14" stroke="url(#iconGrad)" strokeWidth="1.2" />
        <polygon points="4,12 10,10 8,12 10,14" stroke="url(#iconGrad)" strokeWidth="1.2" />
        <polygon points="20,12 14,14 16,12 14,10" stroke="url(#iconGrad)" strokeWidth="1.2" />
        <circle cx="12" cy="12" r="2" stroke="url(#iconGrad)" strokeWidth="1" />
    </IconWrapper>
);

// ── Trending Up Chart — Week 2 Go-to-Market ──
export const ChartUpIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        <rect x="2" y="2" width="20" height="20" rx="2" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <polyline points="6,16 10,11 14,14 18,7" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <polyline points="15,7 18,7 18,10" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="6" y1="19" x2="6" y2="16" stroke="url(#iconGrad)" strokeWidth="1" />
        <line x1="10" y1="19" x2="10" y2="14" stroke="url(#iconGrad)" strokeWidth="1" />
        <line x1="14" y1="19" x2="14" y2="16" stroke="url(#iconGrad)" strokeWidth="1" />
    </IconWrapper>
);

// ── Dollar / Fundraising — Week 3 ──
export const FundraisingIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        <circle cx="12" cy="12" r="10" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <path d="M12 6v12" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <path d="M8 9.5C8 8 9.8 7 12 7s4 1 4 2.5S14.2 12 12 12 8 13 8 14.5 9.8 17 12 17s4-1 4-2.5" stroke="url(#iconGrad)" strokeWidth="1.5" />
    </IconWrapper>
);

// ── Bridge — Week 4 Silicon Valley ──
export const BridgeIcon = ({ size, className }) => (
    <IconWrapper size={size} className={className}>
        {/* Road deck */}
        <line x1="1" y1="16" x2="23" y2="16" stroke="url(#iconGrad)" strokeWidth="1.5" />
        {/* Left tower */}
        <line x1="6" y1="6" x2="6" y2="16" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="8" y1="6" x2="8" y2="16" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="5" y1="6" x2="9" y2="6" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="6" y1="10" x2="8" y2="10" stroke="url(#iconGrad)" strokeWidth="1" />
        <line x1="6" y1="13" x2="8" y2="13" stroke="url(#iconGrad)" strokeWidth="1" />
        {/* Right tower */}
        <line x1="16" y1="6" x2="16" y2="16" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="18" y1="6" x2="18" y2="16" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="15" y1="6" x2="19" y2="6" stroke="url(#iconGrad)" strokeWidth="1.5" />
        <line x1="16" y1="10" x2="18" y2="10" stroke="url(#iconGrad)" strokeWidth="1" />
        <line x1="16" y1="13" x2="18" y2="13" stroke="url(#iconGrad)" strokeWidth="1" />
        {/* Main cable */}
        <path d="M1,10 Q7,16 12,13 Q17,16 23,10" stroke="url(#iconGrad)" strokeWidth="1.5" />
        {/* Water */}
        <path d="M1,19 Q4,18 6,19 Q8,20 10,19 Q12,18 14,19 Q16,20 18,19 Q20,18 23,19" stroke="url(#iconGrad)" strokeWidth="1" />
    </IconWrapper>
);

export default {
    TargetIcon,
    BriefcaseIcon,
    BoltIcon,
    GlobeIcon,
    SoloBuilderIcon,
    RocketIcon,
    CompassIcon,
    ChartUpIcon,
    FundraisingIcon,
    BridgeIcon,
};
