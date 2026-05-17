"use client";

import { useEffect, useRef, useState } from "react";

const EARNEST =
  "i can't stop thinking about what you said about how books are the only place where we're allowed to be other people. i don't know how to say this — i think you might actually be the only person in this city who could read me. sorry this is so much. delete delete delete";
const HEAVY = "I wish you to know that you have been the last dream of my soul. — Dickens";
const REPLY = "(I have read this twice.)";

const LOOP = 22.0;

type InputState = {
  value: string;
  cursor: boolean;
  hesitate?: boolean;
  deleting?: boolean;
  brave?: boolean;
  ready?: boolean;
  sending?: boolean;
};

function phaseInput(t: number): InputState {
  if (t < 0) return { value: "", cursor: true };
  if (t < 2.8) {
    const chars = Math.floor((t / 2.8) * EARNEST.length);
    return { value: EARNEST.slice(0, chars), cursor: true };
  }
  if (t < 4.0) return { value: EARNEST, cursor: true, hesitate: true };
  if (t < 5.8) {
    const remaining = Math.floor(EARNEST.length * (1 - (t - 4.0) / 1.8));
    return { value: EARNEST.slice(0, Math.max(0, remaining)), cursor: true, deleting: true };
  }
  if (t < 7.0) return { value: "", cursor: true, hesitate: true };
  if (t < 9.6) {
    const chars = Math.floor(((t - 7.0) / 2.6) * HEAVY.length);
    return { value: HEAVY.slice(0, chars), cursor: true, brave: true };
  }
  if (t < 10.4) return { value: HEAVY, cursor: true, ready: true };
  if (t < 10.7) return { value: "", cursor: false, sending: true };
  return { value: "", cursor: false };
}

const showSentBubble = (t: number) => t >= 10.5;
const showReply = (t: number) => t >= 12.0;
const dimming = (t: number) => t >= 14.6 && t < 15.6;
const showReveal = (t: number) => t >= 15.6 && t < LOOP;

function useElapsed(): number {
  const [t, setT] = useState(0);
  const startRef = useRef<number>(0);

  useEffect(() => {
    startRef.current = performance.now();
    let raf = 0;
    const tick = () => {
      const elapsed = (performance.now() - startRef.current) / 1000;
      if (elapsed > LOOP) startRef.current = performance.now();
      setT((performance.now() - startRef.current) / 1000);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  return t;
}

function WritingDots() {
  return (
    <div className="writing-dots">
      <span />
      <span />
      <span />
    </div>
  );
}

export default function Scene() {
  const t = useElapsed();
  const tWrap = t % LOOP;

  const input = phaseInput(tWrap);
  const dim = dimming(tWrap);
  const sent = showSentBubble(tWrap);
  const reply = showReply(tWrap);
  const rev = showReveal(tWrap);

  const inputColor = input.brave || input.ready ? "#111" : input.hesitate || input.deleting ? "#666" : "#111";
  const isEmptyPlaceholder = input.value === "" && !input.cursor;

  return (
    <div className="iphone">
      <div className="island" />
      <div className="statusbar">
        <span>9:41</span>
        <span style={{ fontSize: 12, opacity: 0.8 }}>·· ◢ ▮</span>
      </div>

      <div className={`screen ${dim ? "dimming" : ""}`}>
        <div className="msg-header">
          <div className="left">‹ Back</div>
          <div className="who">
            <div className="avatar" />
            <div className="name">L. Moreau</div>
          </div>
          <div className="right">i</div>
        </div>

        <div className="msg-body">
          <div className="msg-date">Tuesday · 9:14 PM</div>

          <div className="msg-bubble from-them">
            Books are the only place where we&apos;re allowed to be other people. That&apos;s all I&apos;m saying.
          </div>

          {sent && (
            <div className="msg-bubble from-me" key="sent">
              I wish you to know that you have been the last dream of my soul.
              <span className="stamp">— Dickens, A Tale of Two Cities</span>
            </div>
          )}

          {reply && (
            <>
              <div style={{ alignSelf: "flex-start" }} key="dots">
                <WritingDots />
              </div>
              <div
                className="msg-bubble from-them"
                key="reply"
                style={{ animation: "bubble-in 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) 0.4s both" }}
              >
                {REPLY}
              </div>
            </>
          )}
        </div>

        <div className="msg-composer">
          <div className="plus">+</div>
          <div className={`msg-input ${isEmptyPlaceholder ? "empty" : ""}`} style={{ color: inputColor }}>
            {input.value || (isEmptyPlaceholder ? "iMessage" : "")}
            {input.cursor && <span className="caret" />}
          </div>
          <div className={`msg-send ${input.ready ? "active" : ""}`}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path
                d="M8 13 L8 3 M4 7 L8 3 L12 7"
                stroke={input.ready ? "#fff" : "rgba(0,0,0,0.4)"}
                strokeWidth="1.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        </div>
      </div>

      <div className="home-indicator" />

      <div className={`reveal ${rev ? "show" : ""}`}>
        <svg width="180" height="180" viewBox="0 0 200 200" aria-label="Asterix">
          <circle cx="100" cy="100" r="82" fill="none" stroke="#B8965A" strokeWidth="1.2" />
          <circle cx="100" cy="100" r="74" fill="none" stroke="#B8965A" strokeWidth="0.6" opacity="0.45" />
          <defs>
            <path id="rv-top" d="M 38 102 A 62 62 0 0 1 162 102" />
            <path id="rv-bot" d="M 38 102 A 62 62 0 0 0 162 102" />
          </defs>
          <text fontFamily="Jost" fontSize="11" letterSpacing="6" fill="#D9CECC" fontWeight="600">
            <textPath href="#rv-top" startOffset="50%" textAnchor="middle">
              ASTERIX  ·  LITERARY POST
            </textPath>
          </text>
          <text fontFamily="Jost" fontSize="11" letterSpacing="6" fill="#D9CECC" fontWeight="600">
            <textPath href="#rv-bot" startOffset="50%" textAnchor="middle">
              ·   MMXXVI   ·
            </textPath>
          </text>
          <g transform="translate(100 100)" stroke="#B8965A" strokeWidth="1.8" strokeLinecap="round" fill="none">
            <line x1="0" y1="-26" x2="0" y2="26" />
            <line x1="-26" y1="0" x2="26" y2="0" />
            <line x1="-18.5" y1="-18.5" x2="18.5" y2="18.5" />
            <line x1="18.5" y1="-18.5" x2="-18.5" y2="18.5" />
          </g>
          <line x1="22" y1="100" x2="68" y2="100" stroke="#B8965A" strokeWidth="0.8" opacity="0.5" />
          <line x1="132" y1="100" x2="178" y2="100" stroke="#B8965A" strokeWidth="0.8" opacity="0.5" />
        </svg>
      </div>
    </div>
  );
}
