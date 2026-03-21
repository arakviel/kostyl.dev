<script setup>
const props = defineProps({
  type: {
    type: String,
    default: 'info', // tip, info, warning, danger
  },
  title: {
    type: String,
    default: '',
  }
})

// Simple inline SVG components or paths
const icons = {
  tip: `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41m11.32-11.32l1.41-1.41M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10z" />
    </svg>
  `,
  info: `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10" />
      <path d="M12 16v-4m0-4h.01" />
    </svg>
  `,
  warning: `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <path d="m12 1.65 10.41 18a2 2 0 0 1-1.73 3H3.32a2 2 0 0 1-1.73-3L12 1.65z" />
      <path d="M12 9v4m0 4h.01" />
    </svg>
  `,
  danger: `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10" />
      <path d="m15 9-6 6M9 9l6 6" />
    </svg>
  `
}
</script>

<template>
  <div :class="['my-10 p-6 rounded-[2rem] border backdrop-blur-3xl transition-all duration-700 not-prose premium-alert group', `alert-${type}`]">
    <!-- Noise & Glow -->
    <div class="alert-noise"></div>
    <div class="alert-glow"></div>

    <!-- Icon Layer -->
    <div class="alert-icon-container">
        <div class="w-6 h-6 text-white icon-svg" v-html="icons[type]"></div>
    </div>
    
    <!-- Content Layer -->
    <div class="flex flex-col gap-1.5 overflow-hidden z-20 w-full relative">
      <div class="flex items-center justify-between w-full mb-0.5">
          <h4 v-if="title" class="alert-title">
            {{ title }}
          </h4>
          <!-- Decorative UI element -->
          <div class="flex gap-1 opacity-20 group-hover:opacity-40 transition-opacity translate-y-[-2px]">
              <div class="w-1.5 h-1.5 rounded-full bg-current"></div>
              <div class="w-1.5 h-1.5 rounded-full bg-current"></div>
          </div>
      </div>
      <div class="alert-content">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.premium-alert {
    position: relative;
    display: flex;
    gap: 1.5rem;
    overflow: hidden;

    /* Default Light Theme */
    --alert-bg: rgba(255, 255, 255, 0.7);
    --alert-border: rgba(0, 0, 0, 0.05);
    --alert-text: #111827;
    --alert-title: #6b7280;
    --alert-accent: #3b82f6;
    --alert-accent-glow: rgba(59, 130, 246, 0.2);
}

:is(.dark *) .premium-alert {
    --alert-bg: rgba(32, 33, 36, 0.7);
    --alert-border: rgba(255, 255, 255, 0.06);
    --alert-text: #f9fafb;
    --alert-title: #9ca3af;
}

/* Color Variants */
.alert-tip { --alert-accent: #10b981; --alert-accent-glow: rgba(16, 185, 129, 0.3); }
.alert-info { --alert-accent: #3b82f6; --alert-accent-glow: rgba(59, 130, 246, 0.3); }
.alert-warning { --alert-accent: #f59e0b; --alert-accent-glow: rgba(245, 158, 11, 0.3); }
.alert-danger { --alert-accent: #f43f5e; --alert-accent-glow: rgba(244, 63, 94, 0.3); }

.premium-alert {
    background-color: var(--alert-bg) !important;
    border: 1px solid var(--alert-border) !important;
    box-shadow: 
        0 10px 15px -3px rgba(0, 0, 0, 0.04),
        0 4px 6px -2px rgba(0, 0, 0, 0.02),
        inset 0 0 0 1px rgba(255, 255, 255, 0.4);
}

.dark .premium-alert {
    box-shadow: 
        0 20px 25px -5px rgba(0, 0, 0, 0.2),
        0 10px 10px -5px rgba(0, 0, 0, 0.1),
        inset 0 0 0 1px rgba(255, 255, 255, 0.02);
}

.alert-noise {
    position: absolute;
    inset: 0;
    z-index: 1;
    opacity: 0.03;
    pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

.alert-glow {
    position: absolute;
    top: -50px;
    left: -50px;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, var(--alert-accent) 0%, transparent 70%);
    filter: blur(40px);
    opacity: 0.1;
    pointer-events: none;
    z-index: 0;
    transition: all 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}

.premium-alert:hover .alert-glow {
    opacity: 0.2;
    transform: scale(1.2) translate(20px, 20px);
}

.alert-icon-container {
    width: 3.25rem;
    height: 3.25rem;
    flex-shrink: 0;
    border-radius: 1.15rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--alert-accent), var(--alert-accent));
    filter: brightness(1.1);
    box-shadow: 
        0 8px 16px -4px var(--alert-accent-glow),
        inset 0 -2px 4px rgba(0,0,0,0.1),
        inset 0 2px 4px rgba(255,255,255,0.2);
    z-index: 10;
    transform: rotate(-3deg);
    transition: transform 0.3s ease;
}

.premium-alert:hover .alert-icon-container {
    transform: rotate(0deg) scale(1.05);
}

.alert-title {
    font-weight: 900;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--alert-title) !important;
    margin: 0 !important;
    line-height: normal;
}

.alert-content {
    font-size: 15px;
    font-weight: 500;
    line-height: 1.6;
    color: var(--alert-text) !important;
    letter-spacing: -0.015em;
}

:deep(p) { margin: 0 !important; }
:deep(code) {
    background: rgba(0, 0, 0, 0.05);
    padding: 0.15em 0.35em;
    border-radius: 8px;
    font-size: 0.85em;
    font-weight: 600;
}
.dark :deep(code) { background: rgba(255, 255, 255, 0.08); }
</style>
