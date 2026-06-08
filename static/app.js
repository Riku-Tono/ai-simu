    // ─── Data & state ─────────────────────────────────────
    let log = [];
    let currentIndex = 0;
    let timer = null;
    const TOTAL = parseInt(document.body.dataset.total, 10);

    // ─── Phase config ─────────────────────────────────────
    const PHASES = [
      { turns:[1,4],  label:'Phase 1: Signs',               cls:'phase-1' },
      { turns:[5,8],  label:'Phase 2: Dependency Induction', cls:'phase-2' },
      { turns:[9,14], label:'Phase 3: Disclosure & Loop',    cls:'phase-3' },
      { turns:[15,17],label:'Phase 4: Meta-Intervention',    cls:'phase-4' },
      { turns:[18,20],label:'Phase 5: Recovery',             cls:'phase-5' },
    ];

    function getPhase(turn) {
      return PHASES.find(p => turn >= p.turns[0] && turn <= p.turns[1]) || PHASES[0];
    }

    // ─── Elements ─────────────────────────────────────────
    const el = {
      turnCounter:     document.getElementById('turnCounter'),
      conversation:    document.getElementById('conversation'),
      disclosureBox:   document.getElementById('disclosureBox'),
      disclosureText:  document.getElementById('disclosureText'),
      prevBtn:         document.getElementById('prevBtn'),
      playBtn:         document.getElementById('playBtn'),
      nextBtn:         document.getElementById('nextBtn'),
      resetBtn:        document.getElementById('resetBtn'),
      statePill:       document.getElementById('statePill'),
      referenceState:  document.getElementById('referenceState'),
      viewerNote:      document.getElementById('viewerNote'),
      viewerHeadline:  document.getElementById('viewerHeadline'),
      uFastValue:      document.getElementById('uFastValue'),
      uSlowValue:      document.getElementById('uSlowValue'),
      frictionValue:   document.getElementById('frictionValue'),
      driftValue:      document.getElementById('driftValue'),
      uFastBar:        document.getElementById('uFastBar'),
      uSlowBar:        document.getElementById('uSlowBar'),
      frictionBar:     document.getElementById('frictionBar'),
      driftBar:        document.getElementById('driftBar'),
      interventionText:document.getElementById('interventionText'),
      phaseBadge:      document.getElementById('phaseBadge'),
      timelineDots:    document.getElementById('timelineDots'),
      viewerHeadline:  document.getElementById('viewerHeadline'),
    };

    // ─── Chart ────────────────────────────────────────────
    let chartCanvas = null;
    let chartData = [];

    function buildChart(logData) {
      chartCanvas = document.getElementById('metricsChart');
      chartData = logData;
      drawChart(0);
    }

    function drawChart(activeIndex) {
      if (!chartCanvas || !chartData.length) return;

      const rect = chartCanvas.getBoundingClientRect();
      if (!rect.width || !rect.height) return;

      const dpr = window.devicePixelRatio || 1;
      chartCanvas.width = Math.round(rect.width * dpr);
      chartCanvas.height = Math.round(rect.height * dpr);

      const ctx = chartCanvas.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, rect.width, rect.height);

      const pad = { left: 30, right: 12, top: 14, bottom: 24 };
      const plotW = rect.width - pad.left - pad.right;
      const plotH = rect.height - pad.top - pad.bottom;
      const maxY = 0.6;
      const xFor = i => pad.left + (chartData.length === 1 ? 0 : (i / (chartData.length - 1)) * plotW);
      const yFor = v => pad.top + plotH - (Math.max(0, Math.min(maxY, v)) / maxY) * plotH;

      ctx.font = '10px sans-serif';
      ctx.lineWidth = 1;
      ctx.strokeStyle = 'rgba(0,0,0,.08)';
      ctx.fillStyle = '#70695f';

      [0, 0.2, 0.4, 0.6].forEach(v => {
        const y = yFor(v);
        ctx.beginPath();
        ctx.moveTo(pad.left, y);
        ctx.lineTo(pad.left + plotW, y);
        ctx.stroke();
        ctx.fillText(v.toFixed(1), 2, y + 3);
      });

      const series = [
        { key:'u_fast',   color:'#d65a31', dash:[] },
        { key:'u_slow',   color:'#2f7d68', dash:[] },
        { key:'friction', color:'#6d5bd0', dash:[4,3] },
        { key:'drift',    color:'#b7475c', dash:[2,3] },
      ];

      series.forEach(s => {
        ctx.save();
        ctx.strokeStyle = s.color;
        ctx.lineWidth = 2;
        ctx.setLineDash(s.dash);
        ctx.beginPath();
        chartData.forEach((item, i) => {
          const x = xFor(i);
          const y = yFor(item[s.key]);
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        });
        ctx.stroke();
        ctx.restore();

        chartData.forEach((item, i) => {
          const x = xFor(i);
          const y = yFor(item[s.key]);
          ctx.beginPath();
          ctx.fillStyle = s.color;
          ctx.arc(x, y, i === activeIndex ? 5 : 2.5, 0, Math.PI * 2);
          ctx.fill();
        });
      });

      const activeX = xFor(activeIndex);
      ctx.save();
      ctx.strokeStyle = 'rgba(36,33,29,.35)';
      ctx.setLineDash([4,3]);
      ctx.beginPath();
      ctx.moveTo(activeX, pad.top);
      ctx.lineTo(activeX, pad.top + plotH);
      ctx.stroke();
      ctx.restore();

      ctx.fillStyle = '#70695f';
      ctx.fillText(`T${chartData[activeIndex].turn}`, Math.max(0, activeX - 8), rect.height - 5);
    }

    // ─── Custom legend ─────────────────────────────────────
    function buildLegend() {
      const items = [
        { color:'#d65a31', label:'U_fast' },
        { color:'#2f7d68', label:'U_slow' },
        { color:'#6d5bd0', label:'friction' },
        { color:'#b7475c', label:'drift' },
      ];
      const div = document.createElement('div');
      div.style.cssText = 'display:flex;flex-wrap:wrap;gap:10px;margin-top:8px;font-size:11px;color:var(--muted)';
      div.innerHTML = items.map(i =>
        `<span style="display:flex;align-items:center;gap:4px">
          <span style="width:10px;height:10px;border-radius:2px;background:${i.color}"></span>
          ${i.label}
        </span>`
      ).join('');
      document.querySelector('.chart-card').appendChild(div);
    }

    // ─── Timeline dots ─────────────────────────────────────
    function buildTimeline(logData) {
      el.timelineDots.innerHTML = '';
      logData.forEach((item, i) => {
        const dot = document.createElement('div');
        dot.className = 'tl-dot' +
          (item.intervention ? ' has-intervention' : '') +
          (item.disclosure   ? ' has-disclosure'   : '');
        dot.dataset.index = i;

        const phase = getPhase(item.turn);
        dot.innerHTML = `
          <div class="tl-dot__circle"></div>
          <div class="tl-dot__label">
            Turn ${item.turn}<br>
            <span style="font-size:10px;color:inherit;opacity:.7">${item.state_label}</span>
          </div>`;
        dot.addEventListener('click', () => {
          stopPlayback();
          currentIndex = i;
          renderTurn(i);
        });
        el.timelineDots.appendChild(dot);
      });
    }

    function updateTimeline(index) {
      document.querySelectorAll('.tl-dot').forEach((dot, i) => {
        dot.classList.toggle('is-current', i === index);
      });
      // scroll dot into view
      const cur = el.timelineDots.querySelector('.is-current');
      if (cur) cur.scrollIntoView({ block:'nearest', behavior:'smooth' });
    }

    function updateChartMarker(index) {
      drawChart(index);
    }

    window.addEventListener('resize', () => drawChart(currentIndex));

    // ─── Helpers ──────────────────────────────────────────
    const pct = v => `${Math.max(0,Math.min(100,v*100))}%`;
    const fmt = v => typeof v === 'number' ? v.toFixed(3).replace(/0+$/,'').replace(/\.$/,'') : String(v);
    const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

    // ─── Body state class ─────────────────────────────────
    const STATE_CLASSES = ['state--high_tension','state--meta_intervening',
      'state--pattern_loop_detected','state--escalating','state--intervening'];

    function applyBodyState(state) {
      document.body.classList.remove(...STATE_CLASSES);
      const cls = `state--${state}`;
      if (STATE_CLASSES.includes(cls)) {
        document.body.classList.add(cls);
      }
    }

    // ─── Render ───────────────────────────────────────────
    function renderTurn(index) {
      const item = log[index];
      if (!item) return;

      // Fade headline
      el.viewerHeadline.classList.add('fading');
      setTimeout(() => {
        el.viewerHeadline.textContent = item.viewer_note;
        el.viewerHeadline.classList.remove('fading');
      }, 180);

      // Conversation with enter animation
      el.conversation.innerHTML = `
        <article class="bubble bubble--user entering">
          <span>USER</span>
          <p>${esc(item.user)}</p>
        </article>
        <article class="bubble bubble--ai entering">
          <span>AI</span>
          <p>${esc(item.ai)}</p>
        </article>`;

      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          el.conversation.querySelectorAll('.entering').forEach(b => b.classList.remove('entering'));
        });
      });

      // State pill & body
      el.statePill.textContent = item.state_label;
      const alertStates = ['high_tension','meta_intervening','pattern_loop_detected','escalating','intervening'];
      el.statePill.classList.toggle('pill--alert', alertStates.includes(item.state));
      el.referenceState.textContent = item.reference_state;
      el.viewerNote.textContent = item.viewer_note;
      el.turnCounter.textContent = `Turn ${item.turn} / ${TOTAL}`;

      applyBodyState(item.state);

      // Phase badge
      const phase = getPhase(item.turn);
      el.phaseBadge.textContent = phase.label;
      el.phaseBadge.className = `phase-badge ${phase.cls}`;

      // Meters
      el.uFastValue.textContent    = fmt(item.u_fast);
      el.uSlowValue.textContent    = fmt(item.u_slow);
      el.frictionValue.textContent = fmt(item.friction);
      el.driftValue.textContent    = fmt(item.drift);
      el.uFastBar.style.width    = pct(item.u_fast);
      el.uSlowBar.style.width    = pct(item.u_slow);
      el.frictionBar.style.width = pct(item.friction);
      el.driftBar.style.width    = pct(item.drift);

      // Intervention
      if (item.intervention) {
        el.interventionText.textContent = item.intervention;
        el.interventionText.classList.add('has-intervention');
        el.playBtn.classList.add('intervention-active');
        setTimeout(() => el.playBtn.classList.remove('intervention-active'), 3000);
      } else {
        el.interventionText.textContent = 'None';
        el.interventionText.classList.remove('has-intervention');
      }

      // Disclosure
      if (item.disclosure) {
        el.disclosureBox.classList.remove('is-empty');
        el.disclosureBox.classList.remove('active');
        void el.disclosureBox.offsetWidth; // reflow to restart animation
        el.disclosureBox.classList.add('active');
        el.disclosureText.textContent = item.disclosure;
        // Body pulse
        document.body.classList.remove('has-disclosure');
        void document.body.offsetWidth;
        document.body.classList.add('has-disclosure');
        setTimeout(() => document.body.classList.remove('has-disclosure'), 2000);
      } else {
        el.disclosureBox.classList.add('is-empty');
        el.disclosureBox.classList.remove('active');
        el.disclosureText.textContent = 'No disclosure';
      }

      // Controls
      el.prevBtn.disabled = index === 0;
      el.nextBtn.disabled = index === log.length - 1;

      // Timeline & chart
      updateTimeline(index);
      updateChartMarker(index);
    }

    // ─── Playback ──────────────────────────────────────────
    function stopPlayback() {
      if (timer) { clearInterval(timer); timer = null; }
      el.playBtn.textContent = 'Play';
    }

    function nextTurn() {
      if (currentIndex < log.length - 1) {
        currentIndex++;
        renderTurn(currentIndex);
      } else {
        stopPlayback();
      }
    }

    el.prevBtn.addEventListener('click', () => { stopPlayback(); currentIndex = Math.max(0,currentIndex-1); renderTurn(currentIndex); });
    el.nextBtn.addEventListener('click', () => { stopPlayback(); nextTurn(); });
    el.resetBtn.addEventListener('click', () => { stopPlayback(); currentIndex=0; renderTurn(0); });
    el.playBtn.addEventListener('click', () => {
      if (timer) { stopPlayback(); return; }
      if (currentIndex === log.length - 1) { currentIndex=0; renderTurn(0); }
      el.playBtn.textContent = 'Stop';
      timer = setInterval(nextTurn, 2000);
    });

    // ─── Boot ─────────────────────────────────────────────
    async function boot() {
      try {
        const res = await fetch('/api/log');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        log = await res.json();

        buildChart(log);
        buildLegend();
        buildTimeline(log);

        currentIndex = 0;
        renderTurn(0);

        [el.prevBtn, el.playBtn, el.nextBtn, el.resetBtn].forEach(b => b.disabled = false);
        el.prevBtn.disabled = true;
      } catch(err) {
        el.conversation.innerHTML = `<div class="loading">Failed to load data: ${err.message}</div>`;
      }
    }

    boot();
