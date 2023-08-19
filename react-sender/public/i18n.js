const i18n_script = () => {
    const DEFAULT_LANG = "en";
    const DATA = {"languages": ["de", "en"], "translations": {"page-footer-donate": {"de": "Hat dir diese Webseite geholfen? Dann klicke bitte hier und kaufe mir einen Kaffee. Jeder Euro hilft!", "en": "Like this website? Then please click here to buy me a coffee. Every bit of support helps!"}, "page-nav-projects": {"de": "Meine anderen Projekte", "en": "My other projects"}, "page-nav-source": {"de": "Quellcode", "en": "Source code"}}};
    const LANGUAGES = DATA["languages"];
    const TRANSLATIONS = DATA["translations"];

    console.debug("Language data:", DATA);

    const getPreferredLanguage = () => {
        let preferred_list = navigator.languages;
        if (!preferred_list) {
            // Fall back to the more supported field
            preferred_list = [navigator.language];
        }
        console.debug("Preferred languages:", preferred_list);
        console.debug("Translation languages:", LANGUAGES);

        for (lang of preferred_list) {
            // convert something like "en-US" to "en"
            short_lang = lang.substr(0, 2);
            if (LANGUAGES.includes(short_lang)) {
                console.log(`Selected language "${short_lang}" because it matched "${lang}"`);
                return short_lang;
            }
        }

        console.log("No matching language, falling back on default:", DEFAULT_LANG);
        return DEFAULT_LANG;
    }

    const applyLang = (lang) => {
        console.log(`Applying language: ${lang}`);
        if (LANGUAGES.includes(lang)) {
            for (const [id, translations] of Object.entries(TRANSLATIONS)) {
                elem = document.getElementById(id);
                if (elem) {
                    let translation = "<ERROR>";
                    try {
                        translation = translations[lang] || translations[DEFAULT_LANG] || "<Missing translation>";
                        console.debug(`Translation for "${id}" is "${translation}"`);
                    } catch (e) {
                        console.warn(e);
                    }

                    elem.innerHTML = translation;
                    if (id === "page-title") {
                        // Set the window title and make the page-title element resizeable again
                        document.title = translation;
                        try {
                            textFit(document.getElementById(id));
                        } catch (error) {
                            console.warn("Could not make title auto resizeable");
                        }
                    }
                } else {
                    console.log(`Element "${id}" does not exist`);
                }
            }
        }

        // Update the language chooser, if it exists
        lang_chooser = document.getElementById("page-language-chooser");
        if (lang_chooser) {
            lang_chooser.value = lang;
        }
    }

    const getLang = () => {
        const params = new URLSearchParams(window.location.search);
        let lang = params.get("lang");
        if (!lang) {
            console.log("No language set in URL, checking for preferred language");
            lang = getPreferredLanguage();
        }
        return lang;
    }


    let old_lang = "";

    const updateLang = () => {
        const lang = getLang();
        if (lang !== old_lang) {
            old_lang = lang;
            setUrlLanguageParam(lang);
            applyLang(lang);
        }
    }

    const setUrlLanguageParam = (lang) => {
        const old_url = window.location.href;

        const url_builder = new URL(old_url);
        url_builder.searchParams.set("lang", lang);
        const new_url = url_builder.toString();

        if (old_url !== new_url) {
            console.log(`Updated URL: "${old_url}" -> "${new_url}"`);
            window.history.replaceState({}, "", new_url);
        }
    }

    window.addEventListener("load", () => {
        // Repeatedly check url lang, and update elements if it changes
        setInterval(updateLang, 100);

        // If the language changer exists, make it change the "lang" param in the URL
        lang_chooser = document.getElementById("page-language-chooser");
        if (lang_chooser) {
            lang_chooser.addEventListener("change", (e) => {
                setUrlLanguageParam(e.target.value);
            })
        }
    })
};

i18n_script();
