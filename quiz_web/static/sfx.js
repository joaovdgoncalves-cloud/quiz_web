/* =================================================================
 * sfx.js — efeitos sonoros leves via Web Audio API
 * (sem arquivos externos; bipes gerados on the fly)
 * ================================================================= */
const SFX = (() => {
  let ctx = null;
  function getCtx() {
    if (!ctx) {
      try { ctx = new (window.AudioContext || window.webkitAudioContext)(); }
      catch (e) { ctx = null; }
    }
    return ctx;
  }

  function tone(freq, duration, type = "sine", volume = 0.15) {
    const c = getCtx();
    if (!c) return;
    const osc = c.createOscillator();
    const gain = c.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    gain.gain.value = volume;
    osc.connect(gain).connect(c.destination);
    osc.start();
    gain.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + duration);
    osc.stop(c.currentTime + duration);
  }

  return {
    click() { tone(660, 0.06, "square", 0.05); },
    correct() {
      tone(523.25, 0.12, "triangle", 0.12);          // C5
      setTimeout(() => tone(659.25, 0.12, "triangle", 0.12), 110);   // E5
      setTimeout(() => tone(783.99, 0.22, "triangle", 0.12), 220);   // G5
    },
    wrong() {
      tone(220, 0.18, "sawtooth", 0.12);
      setTimeout(() => tone(165, 0.22, "sawtooth", 0.12), 130);
    },
    tick() { tone(880, 0.03, "square", 0.04); },
    victory() {
      [523.25, 659.25, 783.99, 1046.50].forEach((f, i) => {
        setTimeout(() => tone(f, 0.18, "triangle", 0.14), i * 140);
      });
    },
  };
})();
