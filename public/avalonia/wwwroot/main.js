import { dotnet } from './_framework/dotnet.js'

const urlParams = new URLSearchParams(window.location.search);
const instanceId = urlParams.get('id');

console.log(`[WASM] main.js initialized for instance: ${instanceId}`);

export function logToVue(message) {
    if (typeof window !== 'undefined') {
        window.parent.postMessage({ type: 'wasm-log', message, id: instanceId }, '*');
    }
}

export function setIframeHeight(height) {
    if (typeof window !== 'undefined') {
        console.log(`[WASM-IPC] Setting height to ${height} for ${instanceId}`);
        window.parent.postMessage({ type: 'set-height', height, id: instanceId }, '*');
    }
}

const is_browser = typeof window != "undefined";
if (!is_browser) throw new Error(`Expected to be running in a browser`);

const dotnetRuntime = await dotnet
    .withDiagnosticTracing(false)
    .withApplicationArgumentsFromQuery()
    .create();

dotnetRuntime.setModuleImports("main.js", {
    logToVue: (message) => logToVue(message),
    setIframeHeight: (height) => setIframeHeight(height)
});

const config = dotnetRuntime.getConfig();

await dotnetRuntime.runMain(config.mainAssemblyName, [globalThis.location.href]);

try {
    const exports = await dotnetRuntime.getAssemblyExports(config.mainAssemblyName);
    
    // Use KostylBridge as defined in Program.cs
    const bridge = exports.KostylBridge || (exports.global ? exports.global.KostylBridge : null);
    
    if (bridge) {
        console.log("KostylBridge Found! Available methods:", Object.keys(bridge));
    } else {
        console.error("Critical: KostylBridge NOT found in exports. Keys:", Object.keys(exports));
    }

    window.addEventListener('message', (event) => {
        if (!event.data || !event.data.type) return;

        if (!bridge) {
            console.error("Bridge is not available.");
            return;
        }

        if (event.data.type === 'ping') {
            window.parent.postMessage({ type: 'avalonia-ready', id: instanceId }, '*');
        } else if (event.data.type === 'update-xaml') {
            console.log("[WASM-JS] Received update-xaml from Vue");
            try {
                if (bridge.UpdateXaml) {
                    console.log("[WASM-JS] Calling KostylBridge.UpdateXaml...");
                    bridge.UpdateXaml(event.data.xaml);
                } else {
                    console.error("[WASM-JS] UpdateXaml not found on bridge");
                }
            } catch (e) {
                console.error("Error calling UpdateXaml:", e);
            }
        } else if (event.data.type === 'set-theme') {
            try {
                if (typeof bridge.SetTheme === 'function') {
                    bridge.SetTheme(event.data.theme);
                } else {
                    console.error("SetTheme is not a function in bridge. Available keys:", Object.keys(bridge));
                }
            } catch (e) {
                console.error("Error calling SetTheme:", e);
            }
        }
    });

    // Initial signal to parent
    window.parent.postMessage({ type: 'avalonia-ready', id: instanceId }, '*');
} catch (err) {
    console.error("Failed to load assembly exports:", err);
}
