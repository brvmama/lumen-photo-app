// LUMEN Masterpiece Photo Enhancer Frontend Logic

document.addEventListener("DOMContentLoaded", () => {
    // State variables
    let currentUpload = null;
    let photographersCatalog = [];
    let currentCategory = "Landscape";
    let isEnhancing = false;
    let uploadedOriginalBaseName = "photo";
    let currentDownloadUrl = "";

    // DOM Elements
    const dropZone = document.getElementById("dropZone");
    const photoInput = document.getElementById("photoInput");
    const uploadPrompt = document.getElementById("uploadPrompt");
    const previewContainer = document.getElementById("previewContainer");
    const imagePreview = document.getElementById("imagePreview");
    const removeImageBtn = document.getElementById("removeImageBtn");

    const contextCard = document.getElementById("contextCard");
    const categoryButtonGroup = document.getElementById("categoryButtonGroup");
    const catPills = document.querySelectorAll(".cat-pill");
    const autoDetectPill = document.getElementById("autoDetectPill");
    const detectedContextName = document.getElementById("detectedContextName");
    const reasoningText = document.getElementById("reasoningText");

    const photographerSelect = document.getElementById("photographerSelect");
    const masterName = document.getElementById("masterName");
    const masterEra = document.getElementById("masterEra");
    const masterTitle = document.getElementById("masterTitle");
    const masterPhilosophy = document.getElementById("masterPhilosophy");
    const acclaimedWorksList = document.getElementById("acclaimedWorksList");

    const intensitySlider = document.getElementById("intensitySlider");
    const intensityLabel = document.getElementById("intensityLabel");

    const userPhoneNumber = document.getElementById("userPhoneNumber");
    const enhanceBtn = document.getElementById("enhanceBtn");
    const enhanceBtnText = document.getElementById("enhanceBtnText");

    const emptyState = document.getElementById("emptyState");
    const processingState = document.getElementById("processingState");
    const resultsStudio = document.getElementById("resultsStudio");

    const comparisonSlider = document.getElementById("comparisonSlider");
    const comparisonClip = document.getElementById("comparisonClip");
    const sliderHandle = document.getElementById("sliderHandle");
    const originalImageDisplay = document.getElementById("originalImageDisplay");
    const enhancedImageDisplay = document.getElementById("enhancedImageDisplay");
    const downloadBtn = document.getElementById("downloadBtn");
    const customFileNameInput = document.getElementById("customFileNameInput");
    const resultsStyleTag = document.getElementById("resultsStyleTag");

    const recipeMetricsGrid = document.getElementById("recipeMetricsGrid");
    const appliedSignatureText = document.getElementById("appliedSignatureText");

    const notificationBanner = document.getElementById("notificationBanner");
    const notifyStatusIcon = document.getElementById("notifyStatusIcon");
    const notifyStatusTitle = document.getElementById("notifyStatusTitle");
    const notifyStatusDesc = document.getElementById("notifyStatusDesc");
    const directActionLink = document.getElementById("directActionLink");

    const settingsModal = document.getElementById("settingsModal");
    const openSettingsBtn = document.getElementById("openSettingsBtn");
    const closeSettingsBtn = document.getElementById("closeSettingsBtn");
    const cancelSettingsBtn = document.getElementById("cancelSettingsBtn");
    const settingsForm = document.getElementById("settingsForm");

    const sampleButtons = document.querySelectorAll(".sample-btn");

    // Initialize: Fetch Master Photographers and Register PWA Service Worker
    fetchPhotographers();
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js').catch(() => {});
    }

    async function fetchPhotographers() {
        try {
            const res = await fetch("/api/photographers");
            const data = await res.json();
            photographersCatalog = data.photographers || [];
            updateCategoryMasters(currentCategory);
        } catch (err) {
            console.error("Failed to load photographers catalog:", err);
        }
    }

    // Category button click handling
    catPills.forEach(pill => {
        pill.addEventListener("click", () => {
            const cat = pill.getAttribute("data-cat");
            selectCategory(cat, false);
        });
    });

    function selectCategory(category, isAuto = false) {
        currentCategory = category;

        // Update pill styling
        catPills.forEach(pill => {
            if (pill.getAttribute("data-cat").toLowerCase() === category.toLowerCase()) {
                pill.className = "cat-pill active flex items-center justify-center gap-1.5 py-2 px-2.5 rounded-xl text-xs font-semibold border transition border-amber-gold bg-amber-gold/20 text-amber-gold shadow-sm";
            } else {
                pill.className = "cat-pill flex items-center justify-center gap-1.5 py-2 px-2.5 rounded-xl text-xs font-semibold border transition border-gray-700 bg-dark-900 text-gray-300 hover:border-gray-500";
            }
        });

        if (isAuto) {
            autoDetectPill.textContent = `Auto-Detected: ${category}`;
            autoDetectPill.className = "text-[11px] px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30";
        } else {
            autoDetectPill.textContent = "Manual Override";
            autoDetectPill.className = "text-[11px] px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-gold border border-amber-500/30";
        }

        updateCategoryMasters(category);
    }

    function updateCategoryMasters(category, preferredPhotographerId = null) {
        const catLower = category.toLowerCase();
        const masters = photographersCatalog.filter(p => p.category.toLowerCase() === catLower);

        photographerSelect.innerHTML = "";

        masters.forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.id;
            opt.textContent = `${p.name} — ${p.title}`;
            if (preferredPhotographerId && p.id === preferredPhotographerId) {
                opt.selected = true;
            }
            photographerSelect.appendChild(opt);
        });

        // Also add an option group for other masters so user has full freedom
        const otherMasters = photographersCatalog.filter(p => p.category.toLowerCase() !== catLower);
        if (otherMasters.length > 0) {
            const optgroup = document.createElement("optgroup");
            optgroup.label = "─── Other Famous Masters ───";
            otherMasters.forEach(p => {
                const opt = document.createElement("option");
                opt.value = p.id;
                opt.textContent = `${p.name} (${p.category} Style)`;
                if (preferredPhotographerId && p.id === preferredPhotographerId) {
                    opt.selected = true;
                }
                optgroup.appendChild(opt);
            });
            photographerSelect.appendChild(optgroup);
        }

        const selectedId = photographerSelect.value;
        if (selectedId) {
            updateSelectedMasterCard(selectedId);
        }
    }

    function updateSelectedMasterCard(photographerId) {
        const p = photographersCatalog.find(item => item.id === photographerId);
        if (!p) return;

        masterName.textContent = p.name;
        masterEra.textContent = p.era;
        masterTitle.textContent = p.title;
        masterPhilosophy.textContent = p.artistic_philosophy;

        acclaimedWorksList.innerHTML = "";
        (p.acclaimed_works || []).forEach(work => {
            const li = document.createElement("li");
            li.textContent = work;
            acclaimedWorksList.appendChild(li);
        });
    }

    photographerSelect.addEventListener("change", (e) => {
        updateSelectedMasterCard(e.target.value);
    });

    // PWA Installation Handling
    let deferredPrompt = null;
    const installPwaBtn = document.getElementById("installPwaBtn");
    const mobileInstallBanner = document.getElementById("mobileInstallBanner");
    const bannerInstallBtn = document.getElementById("bannerInstallBtn");
    const closeBannerBtn = document.getElementById("closeBannerBtn");
    const iosInstallModal = document.getElementById("iosInstallModal");
    const closeIosModalBtn = document.getElementById("closeIosModalBtn");

    const isIos = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;

    if (!isStandalone) {
        // Android / Desktop Chrome PWA prompt
        window.addEventListener("beforeinstallprompt", (e) => {
            e.preventDefault();
            deferredPrompt = e;
            installPwaBtn.classList.remove("hidden");
            mobileInstallBanner.classList.remove("hidden");
        });

        // iOS Safari detection
        if (isIos) {
            installPwaBtn.classList.remove("hidden");
            mobileInstallBanner.classList.remove("hidden");
        }
    }

    function triggerInstall() {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then((choice) => {
                if (choice.outcome === "accepted") {
                    installPwaBtn.classList.add("hidden");
                    mobileInstallBanner.classList.add("hidden");
                }
                deferredPrompt = null;
            });
        } else if (isIos) {
            iosInstallModal.classList.remove("hidden");
        } else {
            alert("To install, tap your browser menu (⋮ or Share) and select 'Add to Home Screen' or 'Install App'.");
        }
    }

    installPwaBtn.addEventListener("click", triggerInstall);
    bannerInstallBtn.addEventListener("click", triggerInstall);

    closeBannerBtn.addEventListener("click", () => {
        mobileInstallBanner.classList.add("hidden");
    });

    closeIosModalBtn.addEventListener("click", () => {
        iosInstallModal.classList.add("hidden");
    });

    // Intensity Slider
    intensitySlider.addEventListener("input", (e) => {
        const val = parseInt(e.target.value, 10);
        let label = `${val}%`;
        if (val <= 40) label += " (Subtle)";
        else if (val <= 70) label += " (Natural)";
        else if (val <= 90) label += " (Balanced)";
        else label += " (Master Signature)";
        intensityLabel.textContent = label;
    });

    // Drag-and-Drop visual styling
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("border-amber-gold");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("border-amber-gold");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("border-amber-gold");
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    photoInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileUpload(e.target.files[0]);
        }
    });

    removeImageBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        resetUpload();
    });

    function resetUpload() {
        currentUpload = null;
        photoInput.value = "";
        previewContainer.classList.add("hidden");
        uploadPrompt.classList.remove("hidden");
        enhanceBtn.disabled = true;
        emptyState.classList.remove("hidden");
        resultsStudio.classList.add("hidden");
        processingState.classList.add("hidden");
        detectedContextName.textContent = "Ready";
        reasoningText.textContent = "";
    }

    async function handleFileUpload(file) {
        if (file && file.name) {
            uploadedOriginalBaseName = file.name.replace(/\.[^/.]+$/, "").replace(/\s+/g, "_");
        } else {
            uploadedOriginalBaseName = "photo";
        }
        const formData = new FormData();
        formData.append("file", file);

        // Show local preview immediately
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            uploadPrompt.classList.add("hidden");
            previewContainer.classList.remove("hidden");
        };
        reader.readAsDataURL(file);

        detectedContextName.textContent = "Analyzing composition...";
        reasoningText.textContent = "Inspecting horizons, luminance, face structures, and colors...";

        try {
            const res = await fetch("/api/upload", {
                method: "POST",
                body: formData
            });

            if (!res.ok) {
                const text = await res.text();
                let detail = "Upload failed";
                try {
                    const parsed = JSON.parse(text);
                    detail = parsed.detail || detail;
                } catch {
                    if (res.status >= 500 || text.includes("<!DOCTYPE")) {
                        detail = "Cannot reach server. Your PC appears to be asleep or offline.";
                    }
                }
                throw new Error(detail);
            }

            const data = await res.json();
            currentUpload = data;

            // Apply context analysis
            const analysis = data.context_analysis;
            detectedContextName.textContent = `${analysis.category} (${Math.round(analysis.confidence * 100)}% match)`;
            reasoningText.textContent = (analysis.reasons || []).join(" • ");

            // Auto-select category
            selectCategory(analysis.category, true);

            // Update master photographer
            if (data.recommended_photographer) {
                updateCategoryMasters(analysis.category, data.recommended_photographer.id);
            }

            enhanceBtn.disabled = false;

        } catch (err) {
            alert("Error analyzing photo: " + err.message);
            resetUpload();
        }
    }

    // Sample Photo Generator for Instant Testing
    sampleButtons.forEach(btn => {
        btn.addEventListener("click", async () => {
            const type = btn.getAttribute("data-type");
            const blob = await generateSampleCanvasImage(type);
            const file = new File([blob], `sample_${type}.jpg`, { type: "image/jpeg" });
            handleFileUpload(file);
        });
    });

    function generateSampleCanvasImage(type) {
        return new Promise((resolve) => {
            const canvas = document.createElement("canvas");
            canvas.width = 800;
            canvas.height = 600;
            const ctx = canvas.getContext("2d");

            if (type === "landscape") {
                // Sky gradient
                const skyGrad = ctx.createLinearGradient(0, 0, 0, 350);
                skyGrad.addColorStop(0, "#1a5276");
                skyGrad.addColorStop(1, "#85c1e9");
                ctx.fillStyle = skyGrad;
                ctx.fillRect(0, 0, 800, 350);

                // Mountain silhouettes
                ctx.fillStyle = "#2c3e50";
                ctx.beginPath();
                ctx.moveTo(0, 350);
                ctx.lineTo(200, 160);
                ctx.lineTo(380, 280);
                ctx.lineTo(550, 120);
                ctx.lineTo(800, 350);
                ctx.closePath();
                ctx.fill();

                // Green terrain
                const hillGrad = ctx.createLinearGradient(0, 350, 0, 600);
                hillGrad.addColorStop(0, "#27ae60");
                hillGrad.addColorStop(1, "#145a32");
                ctx.fillStyle = hillGrad;
                ctx.fillRect(0, 350, 800, 250);

            } else if (type === "portrait") {
                canvas.width = 600;
                canvas.height = 800;
                // Studio backdrop
                const bgGrad = ctx.createRadialGradient(300, 400, 50, 300, 400, 400);
                bgGrad.addColorStop(0, "#3a3d40");
                bgGrad.addColorStop(1, "#181719");
                ctx.fillStyle = bgGrad;
                ctx.fillRect(0, 0, 600, 800);

                // Portrait head/face with warm skin tones
                ctx.fillStyle = "#d49e78";
                ctx.beginPath();
                ctx.ellipse(300, 360, 130, 180, 0, 0, Math.PI * 2);
                ctx.fill();

                // Hair
                ctx.fillStyle = "#221c1a";
                ctx.beginPath();
                ctx.arc(300, 300, 140, Math.PI, 0);
                ctx.fill();

                // Clothing
                ctx.fillStyle = "#2c2a29";
                ctx.beginPath();
                ctx.ellipse(300, 650, 240, 160, 0, 0, Math.PI * 2);
                ctx.fill();

            } else if (type === "architecture") {
                ctx.fillStyle = "#e0e1dd";
                ctx.fillRect(0, 0, 800, 600);

                // Modernist building concrete & glass facade
                ctx.fillStyle = "#1b263b";
                ctx.fillRect(100, 100, 600, 500);

                // Windows grid
                ctx.fillStyle = "#778da9";
                for (let r = 0; r < 5; r++) {
                    for (let c = 0; c < 6; c++) {
                        ctx.fillRect(140 + c * 90, 140 + r * 80, 70, 55);
                    }
                }

            } else { // street
                ctx.fillStyle = "#4a4e69";
                ctx.fillRect(0, 0, 800, 600);

                // Street asphalt
                ctx.fillStyle = "#22223b";
                ctx.fillRect(0, 400, 800, 200);

                // Crosswalk stripes
                ctx.fillStyle = "#f2e9e4";
                for (let i = 0; i < 8; i++) {
                    ctx.fillRect(80 + i * 85, 430, 50, 140);
                }

                // Silhouette walker
                ctx.fillStyle = "#0d1b2a";
                ctx.beginPath();
                ctx.arc(380, 340, 25, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillRect(365, 365, 30, 85);
            }

            canvas.toBlob((blob) => resolve(blob), "image/jpeg", 0.92);
        });
    }

    // Enhance Action
    enhanceBtn.addEventListener("click", async () => {
        if (!currentUpload || isEnhancing) return;

        const selectedPhotographerId = photographerSelect.value;
        const phone = userPhoneNumber.value.trim();
        const selectedChannel = document.querySelector('input[name="notifyChannel"]:checked').value;
        const intensity = parseInt(intensitySlider.value, 10) / 100.0;

        isEnhancing = true;
        emptyState.classList.add("hidden");
        resultsStudio.classList.add("hidden");
        processingState.classList.remove("hidden");

        try {
            const res = await fetch("/api/enhance", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    filename: currentUpload.filename,
                    photographer_id: selectedPhotographerId,
                    intensity: intensity,
                    phone_number: phone || null,
                    notification_channel: selectedChannel
                })
            });

            if (!res.ok) {
                const text = await res.text();
                let detail = "Enhancement failed";
                try {
                    const parsed = JSON.parse(text);
                    detail = parsed.detail || detail;
                } catch {
                    if (res.status >= 500 || text.includes("<!DOCTYPE")) {
                        detail = "Cannot reach server. Your PC is sleeping or offline.";
                    }
                }
                throw new Error(detail);
            }

            const data = await res.json();
            displayResults(data);

        } catch (err) {
            alert("Enhancement error: " + err.message);
            emptyState.classList.remove("hidden");
        } finally {
            isEnhancing = false;
            processingState.classList.add("hidden");
            enhanceBtnText.textContent = "Re-Enhance with Current Settings";
        }
    });

    function displayResults(data) {
        const { enhanced_url, download_url, photographer, enhancement_report, notification } = data;

        // Populate images and download targets
        currentDownloadUrl = download_url;
        originalImageDisplay.src = currentUpload.original_url;
        enhancedImageDisplay.src = `${enhanced_url}?t=${Date.now()}`;
        
        // Suggest intelligent filename based on original photo name and master style
        const cleanPhotographer = photographer.name.replace(/\s+/g, "_");
        const base = uploadedOriginalBaseName && uploadedOriginalBaseName !== "photo" ? uploadedOriginalBaseName : photographer.category;
        customFileNameInput.value = `${base}_${cleanPhotographer}_enhanced`;

        resultsStyleTag.textContent = `${photographer.name} (${enhancement_report.intensity || '85%'})`;

        // Reset split slider to 50%
        setSliderPosition(50);

        // Populate adjustments metrics
        recipeMetricsGrid.innerHTML = "";
        const metrics = enhancement_report.metrics_applied || {};
        for (const [key, value] of Object.entries(metrics)) {
            const card = document.createElement("div");
            card.className = "bg-dark-900/60 p-3 rounded-xl border border-gray-800";
            const formattedKey = key.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
            card.innerHTML = `
                <span class="text-[10px] text-gray-500 uppercase tracking-wider block font-semibold">${formattedKey}</span>
                <span class="text-xs font-bold text-amber-gold">${value}</span>
            `;
            recipeMetricsGrid.appendChild(card);
        }

        appliedSignatureText.textContent = enhancement_report.style_signature;

        // Notification Banner
        if (notification) {
            notificationBanner.classList.remove("hidden");
            const isWhatsApp = notification.channel === "whatsapp";
            
            if (isWhatsApp) {
                notifyStatusIcon.className = "w-10 h-10 rounded-xl bg-green-500/20 text-green-400 flex items-center justify-center text-xl flex-shrink-0";
                notifyStatusIcon.innerHTML = '<i class="fa-brands fa-whatsapp"></i>';
                notifyStatusTitle.textContent = "WhatsApp Notification Ready";
                directActionLink.innerHTML = 'Open in WhatsApp <i class="fa-solid fa-arrow-up-right-from-square ml-1"></i>';
            } else {
                notifyStatusIcon.className = "w-10 h-10 rounded-xl bg-sky-500/20 text-sky-400 flex items-center justify-center text-xl flex-shrink-0";
                notifyStatusIcon.innerHTML = '<i class="fa-solid fa-comment-sms"></i>';
                notifyStatusTitle.textContent = "SMS Notification Ready";
                directActionLink.innerHTML = 'Open SMS Link <i class="fa-solid fa-arrow-up-right-from-square ml-1"></i>';
            }

            notifyStatusDesc.textContent = `Target: ${notification.phone_number} (${notification.method_used})`;
            directActionLink.href = notification.direct_link || "#";
        } else {
            notificationBanner.classList.add("hidden");
        }

        resultsStudio.classList.remove("hidden");
        resultsStudio.scrollIntoView({ behavior: "smooth" });
    }

    // Dynamic Download with Custom Renaming
    downloadBtn.addEventListener("click", async () => {
        if (!currentDownloadUrl) return;

        let customName = customFileNameInput.value.trim();
        if (!customName) {
            customName = "enhanced_masterpiece";
        }
        // Clean filename (remove extensions if typed, sanitize invalid characters)
        customName = customName.replace(/\.(jpg|jpeg|png|webp)$/i, "").replace(/[/\\?%*:|"<>]/g, "_");
        const fullFileName = `${customName}.jpg`;

        const originalBtnHtml = downloadBtn.innerHTML;
        downloadBtn.innerHTML = '<i class="fa-solid fa-spinner animate-spin text-sm"></i> <span>Saving...</span>';
        downloadBtn.disabled = true;

        try {
            // Fetch blob to guarantee custom filename across mobile Chrome & iOS Safari
            const res = await fetch(currentDownloadUrl);
            const blob = await res.blob();
            const blobUrl = URL.createObjectURL(blob);
            const tempLink = document.createElement("a");
            tempLink.href = blobUrl;
            tempLink.download = fullFileName;
            document.body.appendChild(tempLink);
            tempLink.click();
            document.body.removeChild(tempLink);
            setTimeout(() => URL.revokeObjectURL(blobUrl), 2500);
        } catch (err) {
            const tempLink = document.createElement("a");
            tempLink.href = currentDownloadUrl;
            tempLink.download = fullFileName;
            document.body.appendChild(tempLink);
            tempLink.click();
            document.body.removeChild(tempLink);
        } finally {
            downloadBtn.innerHTML = originalBtnHtml;
            downloadBtn.disabled = false;
        }
    });

    // Split Slider Interaction
    let isDraggingSlider = false;

    function setSliderPosition(percentage) {
        const clamped = Math.max(0, Math.min(100, percentage));
        comparisonClip.style.width = `${clamped}%`;
        sliderHandle.style.left = `${clamped}%`;
    }

    function onPointerMove(e) {
        if (!isDraggingSlider) return;
        const rect = comparisonSlider.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const offsetX = clientX - rect.left;
        const percentage = (offsetX / rect.width) * 100;
        setSliderPosition(percentage);
    }

    function startDragging(e) {
        isDraggingSlider = true;
        onPointerMove(e);
    }

    function stopDragging() {
        isDraggingSlider = false;
    }

    comparisonSlider.addEventListener("mousedown", startDragging);
    comparisonSlider.addEventListener("touchstart", startDragging, { passive: true });

    window.addEventListener("mousemove", onPointerMove);
    window.addEventListener("touchmove", onPointerMove, { passive: true });

    window.addEventListener("mouseup", stopDragging);
    window.addEventListener("touchend", stopDragging);

    // Settings Modal
    openSettingsBtn.addEventListener("click", () => {
        settingsModal.classList.remove("hidden");
    });

    closeSettingsBtn.addEventListener("click", () => {
        settingsModal.classList.add("hidden");
    });

    cancelSettingsBtn.addEventListener("click", () => {
        settingsModal.classList.add("hidden");
    });

    settingsForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const sid = document.getElementById("settingAccountSid").value.trim();
        const token = document.getElementById("settingAuthToken").value.trim();
        const sms = document.getElementById("settingSmsNumber").value.trim();
        const wa = document.getElementById("settingWhatsAppNumber").value.trim();

        try {
            const res = await fetch("/api/settings", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    twilio_account_sid: sid || null,
                    twilio_auth_token: token || null,
                    twilio_phone_number: sms || null,
                    twilio_whatsapp_number: wa || null
                })
            });

            if (res.ok) {
                alert("Twilio settings updated successfully!");
                settingsModal.classList.add("hidden");
            } else {
                alert("Failed to update settings.");
            }
        } catch (err) {
            alert("Error saving settings: " + err.message);
        }
    });
});
