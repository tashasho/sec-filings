import Scene from "./Scene";
import Sparkle from "./Sparkle";

export default function HomePage() {
  return (
    <div className="stage">
      <div className="topbar">
        <span className="wm">
          <Sparkle size={12} color="#B8965A" />
          <span>Asterix</span>
        </span>
        <span>Vol. I · Mumbai · MMXXVI</span>
      </div>

      <Scene />

      <div className="brief">
        <div className="eyebrow">Asterix</div>
        <h1 className="tagline">
          <span className="em">For love,</span>
          <br />
          <span className="em">with love.</span>
        </h1>
        <p>
          A dating app for people who write back. One reader a day — chosen by the way they think about books, not the way they look in photographs.
        </p>
        <div className="what">
          You meet through an excerpt. You write to each other in real sentences. The photograph clarifies, slowly, over five letters. By the time you see their face, you already know what they re-read on a train.
        </div>

        <form className="waitlist" action="#">
          <input type="email" placeholder="your name, written legibly" required />
          <button type="submit">
            <span>Reserve a card</span>
            <svg width="16" height="10" viewBox="0 0 16 10" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round">
              <line x1="0" y1="5" x2="14" y2="5" />
              <polyline points="9,1 14,5 9,9" />
            </svg>
          </button>
        </form>
        <div className="micro">
          By invitation
          <span className="dot">·</span>
          iOS, soon
        </div>
      </div>
    </div>
  );
}
