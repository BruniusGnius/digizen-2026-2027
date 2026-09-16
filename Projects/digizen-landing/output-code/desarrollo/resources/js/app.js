import { setupNavigation } from './modules/navigation';
import { setupDialogs } from './modules/dialogs';
import { setupButtons } from './lib/spring';

let config = { mode: 'preview', checkout: {} };
try { config = { ...config, ...JSON.parse(document.querySelector('#digizen-config').textContent) }; }
catch { /* Safe, non-submitting preview if configuration is missing. */ }
setupNavigation();
setupDialogs(config);
setupButtons();
