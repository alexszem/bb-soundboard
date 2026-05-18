import '@mantine/core/styles.css';
import './styles.css';
import { MantineProvider, createTheme } from '@mantine/core';
import { StrictMode, useCallback, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { api } from './api/client';
import type { AudioFile, Player, Snippet, SnippetType } from './api/types';
import { BottomNav, type Page } from './components/BottomNav';
import { NowPlayingBar } from './components/NowPlayingBar';
import { useAudioPlayer } from './hooks/useAudioPlayer';
import { useLocalStorage } from './hooks/useLocalStorage';
import { FilesPage } from './pages/FilesPage';
import { MainPage } from './pages/MainPage';
import { PlayersPage } from './pages/PlayersPage';
import { SnippetsPage } from './pages/SnippetsPage';

const theme = createTheme({
  primaryColor: 'red',
  fontFamily: 'Inter, system-ui, sans-serif',
  colors: {
    red: ['#fff5f5', '#ffe3e3', '#ffc9c9', '#ffa8a8', '#ff8787', '#ff6b6b', '#fa5252', '#f03e3e', '#e03131', '#c92a2a'],
  },
});

function App() {
  const [page, setPage] = useState<Page>('main');
  const [players, setPlayers] = useState<Player[]>([]);
  const [audioFiles, setAudioFiles] = useState<AudioFile[]>([]);
  const [snippets, setSnippets] = useState<Snippet[]>([]);
  const [snippetTypes, setSnippetTypes] = useState<SnippetType[]>([]);
  const [queue, setQueue] = useLocalStorage<string[]>('soundboard-player-queue', []);
  const { playing, play, stop } = useAudioPlayer();

  const reload = useCallback(async () => {
    const [playersResponse, filesResponse, snippetsResponse, typesResponse] = await Promise.all([
      api.listPlayers(),
      api.listAudioFiles(),
      api.listSnippets(),
      api.listSnippetTypes(),
    ]);
    setPlayers(playersResponse);
    setAudioFiles(filesResponse.items);
    setSnippets(snippetsResponse.items);
    setSnippetTypes(typesResponse);
  }, []);

  useEffect(() => {
    reload().catch(console.error);
  }, [reload]);

  return (
    <div className="app-shell">
      <main className="content">
        {page === 'main' && (
          <MainPage
            players={players}
            queue={queue}
            setQueue={setQueue}
            snippetTypes={snippetTypes}
            snippets={snippets}
            audioFiles={audioFiles}
            play={play}
          />
        )}
        {page === 'snippets' && <SnippetsPage audioFiles={audioFiles} snippetTypes={snippetTypes} snippets={snippets} reload={reload} />}
        {page === 'players' && <PlayersPage players={players} snippets={snippets} audioFiles={audioFiles} reload={reload} />}
        {page === 'files' && <FilesPage audioFiles={audioFiles} reload={reload} />}
      </main>
      <NowPlayingBar playing={playing} onStop={stop} />
      <BottomNav active={page} onChange={setPage} />
    </div>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider theme={theme} defaultColorScheme="light">
      <App />
    </MantineProvider>
  </StrictMode>
);
