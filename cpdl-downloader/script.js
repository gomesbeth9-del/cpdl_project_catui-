document.addEventListener('DOMContentLoaded', () => {
    const musicList = document.getElementById('musicList');
    const searchInput = document.getElementById('searchInput');
    const pdfViewer = document.getElementById('pdfViewer');
    const initialMessage = '<p>Selecione uma música para visualizar a partitura.</p>';

    function renderMusicList(filter = '') {
        musicList.innerHTML = '';
        const searchTerm = filter.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");

        const musicMap = new Map();

        musicData.forEach(music => {
            const key = `${music.title}|${music.author}`;
            if (!musicMap.has(key)) {
                musicMap.set(key, {
                    title: music.title,
                    author: music.author,
                    versions: [],
                    hasOrgan: false
                });
            }
            const musicEntry = musicMap.get(key);
            musicEntry.versions.push({
                path: music.path,
                name: music.version
            });
            if (music.version.toLowerCase().includes('orgao') || music.version.toLowerCase().includes('órgão')) {
                musicEntry.hasOrgan = true;
            }
        });

        let musicArray = Array.from(musicMap.values());

        if (searchTerm) {
            musicArray = musicArray.filter(music => {
                const title = music.title.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
                const author = music.author.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
                return title.includes(searchTerm) || author.includes(searchTerm);
            });
        }

        if (musicArray.length === 0) {
            musicList.innerHTML = '<li>Nenhuma música encontrada.</li>';
            return;
        }

        musicArray.sort((a, b) => a.title.localeCompare(b.title));

        musicArray.forEach(music => {
            const li = document.createElement('li');
            
            const titleSpan = document.createElement('div');
            titleSpan.className = 'music-title';
            titleSpan.textContent = music.title;
            
            if (music.author.includes('Catuí')) {
                const catuiTag = document.createElement('span');
                catuiTag.className = 'catui-tag';
                catuiTag.textContent = 'CATUÍ';
                titleSpan.appendChild(catuiTag);
            }

            if (music.hasOrgan) {
                const organTag = document.createElement('span');
                organTag.className = 'organ-tag';
                organTag.textContent = 'ÓRGÃO';
                titleSpan.appendChild(organTag);
            }

            const authorSpan = document.createElement('div');
            authorSpan.className = 'music-author';
            authorSpan.textContent = music.author;

            li.appendChild(titleSpan);
            li.appendChild(authorSpan);

            const versionsList = document.createElement('ul');
            versionsList.className = 'versions-list';
            music.versions.forEach(version => {
                const versionLi = document.createElement('li');
                versionLi.className = 'version-item';
                
                // Decodifica o nome do arquivo para exibição
                let displayName = decodeURIComponent(version.name);
                displayName = displayName.replace(/_/g, ' ').replace(/\.pdf$/i, '');

                versionLi.textContent = displayName;
                versionLi.dataset.pdfPath = version.path;

                versionLi.addEventListener('click', (e) => {
                    e.stopPropagation();
                    document.querySelectorAll('.version-item.active').forEach(item => item.classList.remove('active'));
                    versionLi.classList.add('active');
                    
                    // Garante que o caminho do PDF está corretamente codificado para a URL
                    pdfViewer.innerHTML = `<iframe src="${encodeURI(version.path)}"></iframe>`;
                });
                versionsList.appendChild(versionLi);
            });

            li.appendChild(versionsList);
            musicList.appendChild(li);
        });
    }

    searchInput.addEventListener('input', (e) => {
        renderMusicList(e.target.value);
    });

    pdfViewer.innerHTML = initialMessage;
    renderMusicList();
});
