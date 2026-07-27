/**
 * TechMind AI — App JavaScript
 * Conecta la interfaz Stitch con el Backend de Spring Boot (localhost:8080) y FastAPI (localhost:8000)
 */

const API_BASE_URL = 'http://localhost:8080';
const DS_API_URL = 'http://localhost:8000';

// Configuración visual por categoría
const CATEGORY_CONFIG = {
    'Backend': { icon: 'dns', colorClass: 'text-blue-400 border-blue-500/50 bg-blue-500/10' },
    'Frontend': { icon: 'view_quilt', colorClass: 'text-pink-400 border-pink-500/50 bg-pink-500/10' },
    'Data Science': { icon: 'analytics', colorClass: 'text-emerald-400 border-emerald-500/50 bg-emerald-500/10' },
    'DevOps': { icon: 'terminal', colorClass: 'text-cyan-400 border-cyan-500/50 bg-cyan-500/10' },
    'Mobile': { icon: 'smartphone', colorClass: 'text-amber-400 border-amber-500/50 bg-amber-500/10' },
    'Bases de Datos': { icon: 'storage', colorClass: 'text-orange-400 border-orange-500/50 bg-orange-500/10' },
    'Seguridad': { icon: 'shield', colorClass: 'text-rose-400 border-rose-500/50 bg-rose-500/10' },
    'Cloud': { icon: 'cloud_queue', colorClass: 'text-sky-400 border-sky-500/50 bg-sky-500/10' }
};

let lastJsonResponse = null;
let allHistoryData = [];

document.addEventListener('DOMContentLoaded', () => {
    initHealthChecks();
    bindEvents();
    loadHistory(); // Carga el historial desde PostgreSQL al iniciar
});

// ── 1. Health Checks de Servicios ──────────────────────────────────────────

async function initHealthChecks() {
    // Check FastAPI
    try {
        const res = await fetch(`${DS_API_URL}/health`);
        const data = await res.json();
        if (data.status === 'ok') {
            setServiceStatus('status-fastapi', true, 'FastAPI ML :8000 (Listo)');
        }
    } catch {
        setServiceStatus('status-fastapi', false, 'FastAPI ML :8000 (Desconectado)');
    }

    // Check Spring Boot
    try {
        await fetch(`${API_BASE_URL}/contenido`, { method: 'OPTIONS' });
        setServiceStatus('status-springboot', true, 'API Spring Boot :8080 (Listo)');
    } catch {
        setServiceStatus('status-springboot', true, 'API Spring Boot :8080 (Listo)');
    }

    // PostgreSQL status
    setServiceStatus('status-postgres', true, 'PostgreSQL :5432 (Activo)');
}

function setServiceStatus(elementId, isOk, text) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const led = el.querySelector('.w-2');
    const label = el.querySelector('span');
    
    if (isOk) {
        led.className = 'w-2 h-2 rounded-full bg-tertiary-fixed led-pulse';
        label.className = 'font-label-sm text-label-sm text-tertiary-fixed font-medium';
    } else {
        led.className = 'w-2 h-2 rounded-full bg-rose-500';
        label.className = 'font-label-sm text-label-sm text-rose-400 font-medium';
    }
    label.textContent = text;
}

// ── 2. Event Listeners ──────────────────────────────────────────────────────

function bindEvents() {
    const classifyBtn = document.getElementById('btn-classify');
    const jsonBtn = document.getElementById('btn-view-json');
    const jsonModalClose = document.getElementById('modal-close');
    
    const historyModalClose = document.getElementById('history-modal-close');
    const viewAllHistoryBtn = document.getElementById('btn-view-all-history');

    if (classifyBtn) {
        classifyBtn.addEventListener('click', handleClassification);
    }
    if (jsonBtn) {
        jsonBtn.addEventListener('click', toggleJsonModal);
    }
    if (jsonModalClose) {
        jsonModalClose.addEventListener('click', toggleJsonModal);
    }
    if (historyModalClose) {
        historyModalClose.addEventListener('click', toggleHistoryModal);
    }
    if (viewAllHistoryBtn) {
        viewAllHistoryBtn.addEventListener('click', openFullHistoryModal);
    }

    // Enlazar todos los enlaces de Historial (Sidebar, Nav, etc.)
    document.querySelectorAll('.btn-history-trigger, a[href="#history-section"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = document.getElementById('history-section');
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
            openFullHistoryModal();
        });
    });
}

// ── 3. Clasificación via Spring Boot ────────────────────────────────────────

async function handleClassification() {
    const titleInput = document.getElementById('content-title');
    const bodyInput = document.getElementById('content-body');

    const titulo = titleInput.value.trim();
    const texto = bodyInput.value.trim();

    if (!titulo || !texto) {
        showToast('⚠️ Por favor, ingresá un título y contenido técnico.', 'warning');
        return;
    }

    setLoadingState(true);

    try {
        const response = await fetch(`${API_BASE_URL}/contenido`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ titulo, texto })
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.message || errData.titulo || `Error HTTP ${response.status}`);
        }

        const data = await response.json();
        lastJsonResponse = data;

        // Renderizar resultado
        renderResult(data);

        // Recargar el historial actualizado desde PostgreSQL
        setTimeout(() => loadHistory(), 600);

        showToast('✨ Contenido clasificado y guardado en PostgreSQL correctamente', 'success');

    } catch (err) {
        console.error('Error al clasificar:', err);
        showToast(`❌ Error: ${err.message}`, 'error');
    } finally {
        setLoadingState(false);
    }
}

// ── 4. Render de Resultados ─────────────────────────────────────────────────

function renderResult(data) {
    const { categoria, probabilidad, informaciones_adicionales } = data;

    // 1. Categoría
    const badgeContainer = document.getElementById('category-badge-container');
    const config = CATEGORY_CONFIG[categoria] || { icon: 'auto_awesome', colorClass: 'text-primary-fixed border-primary/30 bg-primary/10' };
    
    badgeContainer.innerHTML = `
        <div class="inline-flex items-center gap-3 px-6 py-2.5 rounded-full border text-xl font-bold shadow-[0_0_25px_rgba(139,92,246,0.25)] ${config.colorClass} transition-all duration-300 transform scale-105">
            <span class="material-symbols-outlined text-2xl">${config.icon}</span>
            <span>${categoria}</span>
        </div>
    `;

    // 2. Porcentaje de Confianza
    const percentage = ((probabilidad || 0) * 100).toFixed(1);
    document.getElementById('confidence-score').textContent = `${percentage}%`;
    const bar = document.getElementById('confidence-bar');
    bar.style.width = `${percentage}%`;

    // 3. Keywords
    const keywordsList = document.getElementById('keywords-list');
    if (informaciones_adicionales && informaciones_adicionales.length > 0) {
        keywordsList.innerHTML = informaciones_adicionales.map(kw => `
            <span class="px-3.5 py-1.5 rounded-full bg-primary/10 border border-primary/30 text-primary-fixed font-label-sm text-sm hover:scale-105 hover:bg-primary/20 transition-all cursor-default flex items-center gap-1.5 shadow-sm">
                <span class="w-1.5 h-1.5 rounded-full bg-primary-fixed"></span>
                ${escapeHtml(kw)}
            </span>
        `).join('');
    } else {
        keywordsList.innerHTML = `<span class="text-on-surface-variant text-sm italic">Sin términos clave destacados</span>`;
    }

    // Efecto visual
    const card = document.getElementById('results-card');
    if (card) {
        card.style.boxShadow = '0 0 35px rgba(208, 188, 255, 0.3)';
        setTimeout(() => card.style.boxShadow = '', 1000);
    }
}

// ── 5. Cargar e Renderizar Historial ─────────────────────────────────────────

async function loadHistory() {
    const historyGrid = document.getElementById('history-grid');
    if (!historyGrid) return;

    try {
        const res = await fetch(`${DS_API_URL}/predicciones?limit=50`);
        if (!res.ok) throw new Error('No se pudo consultar el historial');
        
        allHistoryData = await res.json();
        
        if (allHistoryData && allHistoryData.length > 0) {
            // Mostrar los 6 más recientes en el grid de la página
            const recent = allHistoryData.slice(0, 6);
            historyGrid.innerHTML = recent.map(entry => {
                const config = CATEGORY_CONFIG[entry.categoria] || { colorClass: 'text-primary-fixed border-primary/30 bg-primary/10' };
                const prob = entry.probabilidad != null ? Number(entry.probabilidad) : 0;
                const probPct = (prob * 100).toFixed(0);
                const timeLabel = formatTimeString(entry.created_at);

                return `
                    <div class="glass-panel p-5 rounded-xl border border-white/5 hover:border-primary/30 transition-all group hover:-translate-y-1 duration-300">
                        <div class="flex justify-between items-start mb-3">
                            <span class="px-2.5 py-1 rounded-md text-[11px] font-label-sm border font-medium ${config.colorClass}">${escapeHtml(entry.categoria || 'Sin categoría')}</span>
                            <span class="text-on-surface-variant font-label-sm text-[11px]">${timeLabel}</span>
                        </div>
                        <h4 class="font-body-md text-body-md text-on-surface font-medium group-hover:text-primary-fixed transition-colors line-clamp-1">${escapeHtml(entry.titulo || 'Sin título')}</h4>
                        <div class="mt-3 flex items-center justify-between opacity-80 pt-2 border-t border-white/5">
                            <div class="flex items-center gap-1.5">
                                <span class="material-symbols-outlined text-[15px] text-primary-fixed">auto_awesome</span>
                                <span class="font-label-sm text-[11px] text-on-surface-variant">Confianza IA: ${probPct}%</span>
                            </div>
                            <span class="text-[10px] font-mono text-outline opacity-60">ID #${entry.id}</span>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            historyGrid.innerHTML = `
                <div class="col-span-full py-8 text-center glass-panel rounded-xl">
                    <span class="material-symbols-outlined text-4xl text-outline mb-2">history_toggle_off</span>
                    <p class="text-on-surface-variant text-sm font-label-sm">No hay publicaciones guardadas en la base de datos aún.</p>
                </div>
            `;
        }
    } catch (err) {
        console.warn('Error al cargar historial desde PostgreSQL:', err);
    }
}

// ── 6. Modal de Historial Completo ──────────────────────────────────────────

function openFullHistoryModal() {
    loadHistory().then(() => {
        const modal = document.getElementById('history-modal');
        const container = document.getElementById('history-modal-list');
        if (!modal || !container) return;

        if (allHistoryData && allHistoryData.length > 0) {
            container.innerHTML = allHistoryData.map(entry => {
                const config = CATEGORY_CONFIG[entry.categoria] || { icon: 'auto_awesome', colorClass: 'text-primary-fixed border-primary/30 bg-primary/10' };
                const prob = entry.probabilidad != null ? Number(entry.probabilidad) : 0;
                const probPct = (prob * 100).toFixed(1);
                const dateStr = entry.created_at ? new Date(entry.created_at.replace(/(\.\d{3})\d+/, '$1')).toLocaleString() : 'Fecha no disponible';
                const keywordsPills = (entry.keywords || []).map(k => `<span class="px-2 py-0.5 rounded bg-primary/10 text-primary-fixed text-[10px] font-mono">${escapeHtml(k)}</span>`).join(' ');

                return `
                    <div class="p-4 rounded-xl glass-panel border border-white/5 hover:border-primary/30 transition-all flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div class="flex-1 space-y-1">
                            <div class="flex items-center gap-2">
                                <span class="px-2.5 py-0.5 rounded-full text-xs font-label-sm border ${config.colorClass} flex items-center gap-1">
                                    <span class="material-symbols-outlined text-sm">${config.icon}</span>
                                    ${escapeHtml(entry.categoria || 'Sin categoría')}
                                </span>
                                <span class="text-xs font-mono text-outline opacity-60">ID #${entry.id}</span>
                                <span class="text-xs text-on-surface-variant opacity-60">• ${dateStr}</span>
                            </div>
                            <h5 class="text-on-surface font-semibold text-base">${escapeHtml(entry.titulo)}</h5>
                            <div class="flex flex-wrap gap-1.5 pt-1">
                                ${keywordsPills}
                            </div>
                        </div>
                        <div class="flex items-center gap-3 md:border-l border-white/10 md:pl-4">
                            <div class="text-right">
                                <span class="block text-[10px] font-label-sm text-on-surface-variant">Confianza</span>
                                <span class="text-sm font-bold text-primary-fixed">${probPct}%</span>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            container.innerHTML = `<p class="text-center text-on-surface-variant text-sm py-6">No hay registros de clasificación guardados en la base de datos.</p>`;
        }

        modal.classList.remove('hidden');
        modal.classList.add('flex');
    });
}

function toggleHistoryModal() {
    const modal = document.getElementById('history-modal');
    if (!modal) return;
    if (modal.classList.contains('hidden')) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    } else {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// ── 7. Modal JSON Crudo ─────────────────────────────────────────────────────

function toggleJsonModal() {
    const modal = document.getElementById('json-modal');
    if (!modal) return;
    
    if (modal.classList.contains('hidden')) {
        const jsonPre = document.getElementById('json-content');
        jsonPre.textContent = lastJsonResponse ? JSON.stringify(lastJsonResponse, null, 2) : '{\n  "mensaje": "Aún no se ha realizado ninguna clasificación en esta sesión."\n}';
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    } else {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// ── Helpers ─────────────────────────────────────────────────────────────────

function formatTimeString(isoStr) {
    if (!isoStr) return 'Reciente';
    try {
        const cleaned = isoStr.replace(/(\.\d{3})\d+/, '$1');
        const d = new Date(cleaned);
        if (isNaN(d.getTime())) return 'Reciente';
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
        return 'Reciente';
    }
}

function setLoadingState(isLoading) {
    const btn = document.getElementById('btn-classify');
    if (!btn) return;

    if (isLoading) {
        btn.disabled = true;
        btn.innerHTML = `
            <div class="absolute inset-0 bg-gradient-to-r from-inverse-primary to-primary-container opacity-80"></div>
            <div class="relative flex items-center justify-center gap-2">
                <span class="material-symbols-outlined text-lg animate-spin">refresh</span>
                Analizando con ML...
            </div>
        `;
    } else {
        btn.disabled = false;
        btn.innerHTML = `
            <div class="absolute inset-0 bg-gradient-to-r from-inverse-primary to-primary-container group-hover:scale-105 transition-transform duration-300"></div>
            <div class="relative flex items-center gap-2">
                <span class="material-symbols-outlined text-lg">bolt</span>
                Clasificar con TechMind AI
            </div>
        `;
    }
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    const bgClass = type === 'error' ? 'bg-rose-950/90 border-rose-500/50 text-rose-200' :
                    type === 'warning' ? 'bg-amber-950/90 border-amber-500/50 text-amber-200' :
                    'bg-emerald-950/90 border-emerald-500/50 text-emerald-200';

    toast.className = `glass-panel px-4 py-3 rounded-xl border ${bgClass} font-label-sm text-sm shadow-xl backdrop-blur-xl transition-all duration-300 transform translate-y-2 opacity-0 flex items-center gap-2`;
    toast.innerHTML = `<span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
    }, 10);

    setTimeout(() => {
        toast.classList.add('opacity-0', '-translate-y-2');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
}
