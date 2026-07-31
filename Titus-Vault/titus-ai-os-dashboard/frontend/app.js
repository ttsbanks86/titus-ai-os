/**
 * Titus AI OS Dashboard
 * Main application logic
 */

// API base URL
const API_BASE = 'http://localhost:8000/api';

// Agent data
const AGENTS = [
    { id: 'ceo', name: 'CEO', role: 'Orchestration', status: 'idle' },
    { id: 'engineer', name: 'Engineer', role: 'Engineering', status: 'idle' },
    { id: 'qa', name: 'QA', role: 'Quality Assurance', status: 'idle' },
    { id: 'research', name: 'Research', role: 'Research', status: 'idle' },
    { id: 'reasoning', name: 'Reasoning', role: 'Analysis', status: 'idle' },
    { id: 'browser', name: 'Browser', role: 'Web Automation', status: 'idle' },
    { id: 'automation', name: 'Automation', role: 'Automation', status: 'idle' },
    { id: 'documentation', name: 'Docs', role: 'Documentation', status: 'idle' },
];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    renderAgentGrid();
    loadProjects();
});

// Navigation
function initNavigation() {
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const view = link.dataset.view;
            switchView(view);
        });
    });
}

function switchView(viewId) {
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.dataset.view === viewId);
    });
    
    // Update views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.toggle('active', view.id === viewId);
    });
}

// Render agent grid
function renderAgentGrid() {
    const grid = document.getElementById('agent-grid');
    if (!grid) return;
    
    grid.innerHTML = AGENTS.map(agent => `
        <div class="card">
            <div class="card-header">
                <span class="overline">${agent.role}</span>
                <span class="status-dot status-${agent.status}"></span>
            </div>
            <h3>${agent.name}</h3>
            <p class="text-muted">${agent.status === 'idle' ? 'Ready' : 'Working'}</p>
        </div>
    `).join('');
}

// Load projects
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/projects/`);
        const data = await response.json();
        
        const grid = document.getElementById('projects-grid');
        if (grid && data.projects) {
            grid.innerHTML = data.projects.map(project => `
                <div class="card">
                    <div class="card-header">
                        <span class="overline">${project.status}</span>
                    </div>
                    <h3>${project.name}</h3>
                    <p class="text-muted">${project.phase || 'Active'}</p>
                </div>
            `).join('');
        }
    } catch (error) {
        console.log('API not available, using static data');
    }
}

// Quick actions
async function runAction(actionId) {
    const actionNames = {
        'run-tests': 'Running tests...',
        'refresh-index': 'Refreshing knowledge index...',
        'assemble-context': 'Assembling context...',
        'open-sot': 'Opening Source of Truth...',
    };
    
    alert(actionNames[actionId] || 'Action triggered');
}

// Assemble context
async function assembleContext() {
    const role = document.getElementById('context-role').value;
    const resultDiv = document.getElementById('context-result');
    
    try {
        const response = await fetch(`${API_BASE}/knowledge/context?role=${role}&budget=4000`);
        const data = await response.json();
        
        resultDiv.innerHTML = `
            <div class="card">
                <p><strong>Documents:</strong> ${data.documents || 0}</p>
                <p><strong>Tokens Used:</strong> ${data.tokens_used || 0}</p>
                <p><strong>Budget:</strong> ${data.budget || 4000}</p>
            </div>
        `;
    } catch (error) {
        resultDiv.innerHTML = '<p class="text-muted">API not available</p>';
    }
}
