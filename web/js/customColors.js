import { app } from "../../../scripts/app.js";
import { $el } from "../../../scripts/ui.js";

const colorShade = (col, amt) => {
    col = col.replace(/^#/, "");
    if (col.length === 3) col = col[0] + col[0] + col[1] + col[1] + col[2] + col[2];

    let [r, g, b] = col.match(/.{2}/g);
    [r, g, b] = [
        parseInt(r, 16) + amt,
        parseInt(g, 16) + amt,
        parseInt(b, 16) + amt,
    ];

    r = Math.max(Math.min(255, r), 0).toString(16);
    g = Math.max(Math.min(255, g), 0).toString(16);
    b = Math.max(Math.min(255, b), 0).toString(16);

    const rr = (r.length < 2 ? "0" : "") + r;
    const gg = (g.length < 2 ? "0" : "") + g;
    const bb = (b.length < 2 ? "0" : "") + b;

    return `#${rr}${gg}${bb}`;
};

const normalizeHex = (value, fallback = "#89b4fa") => {
    if (!value) return fallback;
    let v = String(value).trim();

    if (!v.startsWith("#")) v = "#" + v;

    if (/^#([0-9a-fA-F]{3})$/.test(v)) {
        v = "#" + v.slice(1).split("").map((c) => c + c).join("");
    }

    if (/^#([0-9a-fA-F]{6})$/.test(v)) {
        return v.toLowerCase();
    }

    return fallback;
};

const getTargets = (clickedNode) => {
    const graphcanvas = LGraphCanvas.active_canvas;
    if (!graphcanvas?.selected_nodes || Object.keys(graphcanvas.selected_nodes).length <= 1) {
        return [clickedNode];
    }
    return Object.values(graphcanvas.selected_nodes);
};

const getPrimarySelectedNode = () => {
    const canvas = LGraphCanvas.active_canvas;
    const selected = canvas?.selected_nodes ? Object.values(canvas.selected_nodes) : [];
    return selected[0] || null;
};

const captureNodeStates = (clickedNode) => {
    return getTargets(clickedNode).map((node) => ({
        node,
        color: node.color,
        bgcolor: node.bgcolor,
    }));
};

const restoreNodeStates = (states) => {
    for (const state of states) {
        state.node.color = state.color;
        state.node.bgcolor = state.bgcolor;
        state.node.setDirtyCanvas(true, true);
    }
};

const PRESET_PALETTES = {
    "Catppuccin Title Safe": [
        { name: "Blue", hex: "#89b4fa" },
        { name: "Sapphire", hex: "#74c7ec" },
        { name: "Sky", hex: "#89dceb" },
        { name: "Teal", hex: "#94e2d5" },
        { name: "Mauve", hex: "#cba6f7" },
        { name: "Red", hex: "#f38ba8" },
        { name: "Peach", hex: "#fab387" },
        { name: "Overlay", hex: "#6c7086" },
    ],
    "Favorites": [
        { name: "Blue", hex: "#89b4fa" },
        { name: "Lavender", hex: "#b4befe" },
        { name: "Mauve", hex: "#cba6f7" },
        { name: "Teal", hex: "#94e2d5" },
        { name: "Green", hex: "#a6e3a1" },
        { name: "Yellow", hex: "#f9e2af" },
        { name: "Peach", hex: "#fab387" },
        { name: "Red", hex: "#f38ba8" },
    ],
    "Catppuccin Mocha": [
        { name: "Rosewater", hex: "#f5e0dc" },
        { name: "Flamingo", hex: "#f2cdcd" },
        { name: "Pink", hex: "#f5c2e7" },
        { name: "Mauve", hex: "#cba6f7" },
        { name: "Red", hex: "#f38ba8" },
        { name: "Maroon", hex: "#eba0ac" },
        { name: "Peach", hex: "#fab387" },
        { name: "Yellow", hex: "#f9e2af" },
        { name: "Green", hex: "#a6e3a1" },
        { name: "Teal", hex: "#94e2d5" },
        { name: "Sky", hex: "#89dceb" },
        { name: "Sapphire", hex: "#74c7ec" },
        { name: "Blue", hex: "#89b4fa" },
        { name: "Lavender", hex: "#b4befe" },
    ],
    "Catppuccin Macchiato": [
        { name: "Rosewater", hex: "#f4dbd6" },
        { name: "Flamingo", hex: "#f0c6c6" },
        { name: "Pink", hex: "#f5bde6" },
        { name: "Mauve", hex: "#c6a0f6" },
        { name: "Red", hex: "#ed8796" },
        { name: "Maroon", hex: "#ee99a0" },
        { name: "Peach", hex: "#f5a97f" },
        { name: "Yellow", hex: "#eed49f" },
        { name: "Green", hex: "#a6da95" },
        { name: "Teal", hex: "#8bd5ca" },
        { name: "Sky", hex: "#91d7e3" },
        { name: "Sapphire", hex: "#7dc4e4" },
        { name: "Blue", hex: "#8aadf4" },
        { name: "Lavender", hex: "#b7bdf8" },
    ],
    "Nord": [
        { name: "Polar Night 1", hex: "#2e3440" },
        { name: "Polar Night 2", hex: "#3b4252" },
        { name: "Polar Night 3", hex: "#434c5e" },
        { name: "Polar Night 4", hex: "#4c566a" },
        { name: "Snow Storm 1", hex: "#d8dee9" },
        { name: "Snow Storm 2", hex: "#e5e9f0" },
        { name: "Snow Storm 3", hex: "#eceff4" },
        { name: "Frost 1", hex: "#8fbcbb" },
        { name: "Frost 2", hex: "#88c0d0" },
        { name: "Frost 3", hex: "#81a1c1" },
        { name: "Frost 4", hex: "#5e81ac" },
        { name: "Red", hex: "#bf616a" },
        { name: "Orange", hex: "#d08770" },
        { name: "Yellow", hex: "#ebcb8b" },
        { name: "Green", hex: "#a3be8c" },
        { name: "Purple", hex: "#b48ead" },
    ],
    "Gruvbox Dark": [
        { name: "Dark0", hex: "#282828" },
        { name: "Dark1", hex: "#3c3836" },
        { name: "Dark2", hex: "#504945" },
        { name: "Dark3", hex: "#665c54" },
        { name: "Light0", hex: "#fbf1c7" },
        { name: "Light1", hex: "#ebdbb2" },
        { name: "Light2", hex: "#d5c4a1" },
        { name: "Light3", hex: "#bdae93" },
        { name: "Red", hex: "#fb4934" },
        { name: "Green", hex: "#b8bb26" },
        { name: "Yellow", hex: "#fabd2f" },
        { name: "Blue", hex: "#83a598" },
        { name: "Purple", hex: "#d3869b" },
        { name: "Aqua", hex: "#8ec07c" },
        { name: "Orange", hex: "#fe8019" },
    ],
};

const showHexColorDialog = ({
    title,
    initialColor,
    onPreview,
    onApply,
    onCancel,
    onClear,
}) => {
    const startColor = normalizeHex(initialColor);
    let lastValid = startColor;
    let selectedPalette = "Catppuccin Title Safe";
    let applied = false;
    let cleared = false;

    const overlay = $el("div", {
        parent: document.body,
        style: {
            position: "fixed",
            inset: "0",
            background: "rgba(0,0,0,0.45)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: "999999",
        },
    });

    const modal = $el("div", {
        parent: overlay,
        style: {
            width: "360px",
            maxHeight: "80vh",
            overflowY: "auto",
            background: "#1e1e2e",
            color: "#cdd6f4",
            border: "1px solid #45475a",
            borderRadius: "12px",
            boxShadow: "0 18px 48px rgba(0,0,0,0.45)",
            padding: "14px",
            fontFamily: "sans-serif",
        },
    });

    $el("div", {
        parent: modal,
        textContent: title,
        style: {
            fontSize: "14px",
            fontWeight: "600",
            marginBottom: "12px",
        },
    });

    const row = $el("div", {
        parent: modal,
        style: {
            display: "flex",
            gap: "10px",
            alignItems: "center",
            marginBottom: "12px",
        },
    });

    const picker = $el("input", {
        parent: row,
        type: "color",
        value: startColor,
        style: {
            width: "52px",
            height: "40px",
            padding: "0",
            border: "none",
            background: "transparent",
            cursor: "pointer",
        },
    });

    const hexInput = $el("input", {
        parent: row,
        type: "text",
        value: startColor,
        placeholder: "#89b4fa",
        style: {
            flex: "1",
            height: "40px",
            padding: "0 10px",
            borderRadius: "8px",
            border: "1px solid #585b70",
            background: "#11111b",
            color: "#cdd6f4",
            outline: "none",
        },
    });

    const preview = $el("div", {
        parent: modal,
        style: {
            height: "36px",
            borderRadius: "8px",
            background: startColor,
            border: "1px solid #585b70",
            marginBottom: "12px",
        },
    });

    $el("div", {
        parent: modal,
        textContent: "Palette",
        style: {
            fontSize: "12px",
            opacity: "0.85",
            marginBottom: "6px",
        },
    });

    const paletteSelect = $el("select", {
        parent: modal,
        style: {
            width: "100%",
            height: "36px",
            padding: "0 10px",
            borderRadius: "8px",
            border: "1px solid #585b70",
            background: "#11111b",
            color: "#cdd6f4",
            marginBottom: "10px",
            outline: "none",
        },
    });

    for (const name of Object.keys(PRESET_PALETTES)) {
        $el("option", {
            parent: paletteSelect,
            value: name,
            textContent: name,
        });
    }
    paletteSelect.value = selectedPalette;

    const swatchGrid = $el("div", {
        parent: modal,
        style: {
            display: "grid",
            gridTemplateColumns: "repeat(7, 1fr)",
            gap: "6px",
            marginBottom: "12px",
        },
    });

    const favoritesRow = $el("div", {
        parent: modal,
        style: {
            marginBottom: "12px",
        },
    });

    $el("div", {
        parent: favoritesRow,
        textContent: "Quick favorites",
        style: {
            fontSize: "12px",
            opacity: "0.85",
            marginBottom: "6px",
        },
    });

    const favoritesGrid = $el("div", {
        parent: favoritesRow,
        style: {
            display: "grid",
            gridTemplateColumns: "repeat(8, 1fr)",
            gap: "6px",
        },
    });

    const makeSwatch = (parent, swatch) => {
        return $el("button", {
            parent,
            title: `${swatch.name} ${swatch.hex}`,
            style: {
                height: "24px",
                borderRadius: "6px",
                border: "1px solid #585b70",
                background: swatch.hex,
                cursor: "pointer",
            },
            onclick: (e) => {
                e.preventDefault();
                cleared = false;
                setPreview(swatch.hex);
            },
        });
    };

    const renderPalette = (paletteName) => {
        swatchGrid.innerHTML = "";
        for (const swatch of PRESET_PALETTES[paletteName] || []) {
            makeSwatch(swatchGrid, swatch);
        }
    };

    for (const swatch of PRESET_PALETTES["Favorites"]) {
        makeSwatch(favoritesGrid, swatch);
    }

    const setPreview = (value) => {
        const hex = normalizeHex(value, lastValid);
        lastValid = hex;
        picker.value = hex;
        hexInput.value = hex;
        preview.style.background = hex;
        onPreview?.(hex);
    };

    picker.oninput = () => {
        cleared = false;
        setPreview(picker.value);
    };

    hexInput.oninput = () => {
        const raw = hexInput.value.trim();
        if (/^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.test(raw)) {
            cleared = false;
            setPreview(raw);
        }
    };

    paletteSelect.onchange = () => {
        selectedPalette = paletteSelect.value;
        renderPalette(selectedPalette);
    };

    const close = (cancelled = true) => {
        overlay.remove();
        if (cancelled && !applied) {
            onCancel?.();
        }
    };

    const buttonRow = $el("div", {
        parent: modal,
        style: {
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: "8px",
        },
    });

    const leftButtons = $el("div", {
        parent: buttonRow,
        style: {
            display: "flex",
            gap: "8px",
        },
    });

    const rightButtons = $el("div", {
        parent: buttonRow,
        style: {
            display: "flex",
            gap: "8px",
        },
    });

    $el("button", {
        parent: leftButtons,
        textContent: "Reset",
        style: {
            height: "34px",
            padding: "0 12px",
            borderRadius: "8px",
            border: "1px solid #585b70",
            background: "#181825",
            color: "#cdd6f4",
            cursor: "pointer",
        },
        onclick: () => {
            cleared = false;
            setPreview(startColor);
        },
    });

    $el("button", {
        parent: leftButtons,
        textContent: "Clear",
        style: {
            height: "34px",
            padding: "0 12px",
            borderRadius: "8px",
            border: "1px solid #f38ba8",
            background: "#f38ba8",
            color: "#11111b",
            fontWeight: "600",
            cursor: "pointer",
        },
        onclick: () => {
            cleared = true;
            onClear?.();
            preview.style.background = "transparent";
            hexInput.value = "";
        },
    });

    $el("button", {
        parent: rightButtons,
        textContent: "Cancel",
        style: {
            height: "34px",
            padding: "0 12px",
            borderRadius: "8px",
            border: "1px solid #585b70",
            background: "#313244",
            color: "#cdd6f4",
            cursor: "pointer",
        },
        onclick: () => close(true),
    });

    $el("button", {
        parent: rightButtons,
        textContent: "Apply",
        style: {
            height: "34px",
            padding: "0 12px",
            borderRadius: "8px",
            border: "1px solid #89b4fa",
            background: "#89b4fa",
            color: "#11111b",
            fontWeight: "600",
            cursor: "pointer",
        },
        onclick: () => {
            applied = true;
            if (!cleared) {
                onApply?.(lastValid);
            }
            close(false);
        },
    });

    overlay.onclick = (e) => {
        if (e.target === overlay) close(true);
    };

    hexInput.onkeydown = (e) => {
        if (e.key === "Enter") {
            applied = true;
            if (!cleared) {
                onApply?.(lastValid);
            }
            close(false);
        } else if (e.key === "Escape") {
            close(true);
        }
    };

    renderPalette(selectedPalette);
    setPreview(startColor);
};

app.registerExtension({
    name: "minglee.CustomColors",

    commands: [
        {
            id: "minglee.openTitleColorDialog",
            label: "Custom Colors: Open title color dialog",
            function: () => {
                const node = getPrimarySelectedNode();
                if (!node) return;

                const previousStates = captureNodeStates(node);

                const applyTitleColor = (clickedNode, hex) => {
                    for (const n of getTargets(clickedNode)) {
                        n.color = hex;
                        n.setDirtyCanvas(true, true);
                    }
                };

                const clearTitleColor = (clickedNode) => {
                    for (const n of getTargets(clickedNode)) {
                        n.color = null;
                        n.setDirtyCanvas(true, true);
                    }
                };

                showHexColorDialog({
                    title: "Custom Title Color",
                    initialColor: node?.color || "#777777",
                    onPreview: (hex) => applyTitleColor(node, hex),
                    onApply: (hex) => applyTitleColor(node, hex),
                    onCancel: () => restoreNodeStates(previousStates),
                    onClear: () => clearTitleColor(node),
                });
            },
        },
        {
            id: "minglee.openBGColorDialog",
            label: "Custom Colors: Open background color dialog",
            function: () => {
                const node = getPrimarySelectedNode();
                if (!node) return;

                const previousStates = captureNodeStates(node);

                const applyBGColor = (clickedNode, hex) => {
                    for (const n of getTargets(clickedNode)) {
                        n.bgcolor = hex;
                        n.setDirtyCanvas(true, true);
                    }
                };

                const clearBGColor = (clickedNode) => {
                    for (const n of getTargets(clickedNode)) {
                        n.bgcolor = null;
                        n.setDirtyCanvas(true, true);
                    }
                };

                showHexColorDialog({
                    title: "Custom BG Color",
                    initialColor: node?.bgcolor || "#444444",
                    onPreview: (hex) => applyBGColor(node, hex),
                    onApply: (hex) => applyBGColor(node, hex),
                    onCancel: () => restoreNodeStates(previousStates),
                    onClear: () => clearBGColor(node),
                });
            },
        },
        {
            id: "minglee.openFullColorDialog",
            label: "Custom Colors: Open full color dialog",
            function: () => {
                const node = getPrimarySelectedNode();
                if (!node) return;

                const previousStates = captureNodeStates(node);

                const applyFullColor = (clickedNode, hex) => {
                    for (const n of getTargets(clickedNode)) {
                        if (n.constructor === LiteGraph.LGraphGroup) {
                            n.color = hex;
                        } else {
                            const titleHex = colorShade(hex, 20);
                            n.color = titleHex;
                            n.bgcolor = hex;
                        }
                        n.setDirtyCanvas(true, true);
                    }
                };

                const clearFullColor = (clickedNode) => {
                    for (const n of getTargets(clickedNode)) {
                        n.color = null;
                        n.bgcolor = null;
                        n.setDirtyCanvas(true, true);
                    }
                };

                showHexColorDialog({
                    title: "Custom Full Color",
                    initialColor: node?.bgcolor || "#444444",
                    onPreview: (hex) => applyFullColor(node, hex),
                    onApply: (hex) => applyFullColor(node, hex),
                    onCancel: () => restoreNodeStates(previousStates),
                    onClear: () => clearFullColor(node),
                });
            },
        },
    ],

    setup() {
        const onMenuNodeColors = LGraphCanvas.onMenuNodeColors;

        const applyFullColor = (clickedNode, hex) => {
            for (const node of getTargets(clickedNode)) {
                if (node.constructor === LiteGraph.LGraphGroup) {
                    node.color = hex;
                } else {
                    const titleHex = colorShade(hex, 20);
                    node.color = titleHex;
                    node.bgcolor = hex;
                }
                node.setDirtyCanvas(true, true);
            }
        };

        const clearFullColor = (clickedNode) => {
            for (const node of getTargets(clickedNode)) {
                node.color = null;
                node.bgcolor = null;
                node.setDirtyCanvas(true, true);
            }
        };

        const applyTitleColor = (clickedNode, hex) => {
            for (const node of getTargets(clickedNode)) {
                node.color = hex;
                node.setDirtyCanvas(true, true);
            }
        };

        const clearTitleColor = (clickedNode) => {
            for (const node of getTargets(clickedNode)) {
                node.color = null;
                node.setDirtyCanvas(true, true);
            }
        };

        const applyBGColor = (clickedNode, hex) => {
            for (const node of getTargets(clickedNode)) {
                node.bgcolor = hex;
                node.setDirtyCanvas(true, true);
            }
        };

        const clearBGColor = (clickedNode) => {
            for (const node of getTargets(clickedNode)) {
                node.bgcolor = null;
                node.setDirtyCanvas(true, true);
            }
        };

        LGraphCanvas.onMenuNodeColors = function (value, options, e, menu, node) {
            const r = onMenuNodeColors.apply(this, arguments);

            requestAnimationFrame(() => {
                const menus = document.querySelectorAll(".litecontextmenu");
                for (let i = menus.length - 1; i >= 0; i--) {
                    const first = menus[i].firstElementChild;
                    const text = first?.textContent || "";
                    const content = first?.value?.content || "";

                    if (text.includes("No color") || content.includes("No color")) {
                        $el("div.litemenu-entry.submenu", {
                            parent: menus[i],
                            $: (el) => {
                                el.onclick = () => {
                                    LiteGraph.closeAllContextMenus();
                                    const previousStates = captureNodeStates(node);

                                    showHexColorDialog({
                                        title: "Custom Full Color",
                                        initialColor: node?.bgcolor || "#444444",
                                        onPreview: (hex) => applyFullColor(node, hex),
                                        onApply: (hex) => applyFullColor(node, hex),
                                        onCancel: () => restoreNodeStates(previousStates),
                                        onClear: () => clearFullColor(node),
                                    });
                                };
                            },
                        }, [
                            $el("span", {
                                style: { paddingLeft: "4px", display: "block" },
                                textContent: "🎨 Custom Full",
                            }),
                        ]);

                        $el("div.litemenu-entry.submenu", {
                            parent: menus[i],
                            $: (el) => {
                                el.onclick = () => {
                                    LiteGraph.closeAllContextMenus();
                                    const previousStates = captureNodeStates(node);

                                    showHexColorDialog({
                                        title: "Custom Title Color",
                                        initialColor: node?.color || "#777777",
                                        onPreview: (hex) => applyTitleColor(node, hex),
                                        onApply: (hex) => applyTitleColor(node, hex),
                                        onCancel: () => restoreNodeStates(previousStates),
                                        onClear: () => clearTitleColor(node),
                                    });
                                };
                            },
                        }, [
                            $el("span", {
                                style: { paddingLeft: "4px", display: "block" },
                                textContent: "🎨 Custom Title",
                            }),
                        ]);

                        $el("div.litemenu-entry.submenu", {
                            parent: menus[i],
                            $: (el) => {
                                el.onclick = () => {
                                    LiteGraph.closeAllContextMenus();
                                    const previousStates = captureNodeStates(node);

                                    showHexColorDialog({
                                        title: "Custom BG Color",
                                        initialColor: node?.bgcolor || "#444444",
                                        onPreview: (hex) => applyBGColor(node, hex),
                                        onApply: (hex) => applyBGColor(node, hex),
                                        onCancel: () => restoreNodeStates(previousStates),
                                        onClear: () => clearBGColor(node),
                                    });
                                };
                            },
                        }, [
                            $el("span", {
                                style: { paddingLeft: "4px", display: "block" },
                                textContent: "🎨 Custom BG",
                            }),
                        ]);

                        break;
                    }
                }
            });

            return r;
        };
    },
});