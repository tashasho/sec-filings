type SparkleProps = {
  size?: number;
  color?: string;
};

export default function Sparkle({ size = 14, color = "currentColor" }: SparkleProps) {
  const c = size / 2;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ display: "inline-block" }}>
      <path
        d={`M ${c} 0 C ${c} ${c * 0.6} ${c * 0.6} ${c} 0 ${c} C ${c * 0.6} ${c} ${c} ${c * 1.4} ${c} ${size} C ${c} ${c * 1.4} ${c * 1.4} ${c} ${size} ${c} C ${c * 1.4} ${c} ${c} ${c * 0.6} ${c} 0 Z`}
        fill={color}
      />
    </svg>
  );
}
