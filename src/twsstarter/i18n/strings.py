from __future__ import annotations

# Supported languages = the languages Interactive Brokers TWS ships in.
# This dict is the single source of truth for the selectable set (see
# i18n.set_language / detect_language). Translation data for other languages may
# still exist in STRINGS below but is not selectable.
LANGUAGES: dict[str, str] = {
    'en': 'English',
    'de': 'Deutsch',
    'fr': 'Français',
    'es': 'Español',
    'it': 'Italiano',
    'ru': 'Русский',
    'nl': 'Nederlands',
    'pt': 'Português',
    'zh': '中文',
    'ja': '日本語',
}

# ── Help texts (HTML) ──────────────────────────────────────────────────────

_HELP = {
'en': """
<h2>TWSStarter</h2>
<p>TWSStarter is a <b>launcher</b> for Interactive Brokers <b>Trader WorkStation (TWS)</b>
and <b>IB Gateway</b>. Its sole purpose is to start TWS or Gateway conveniently —
including multiple installations or different versions side by side — and to fill
in your login credentials automatically.</p>

<p><b>TWSStarter does not monitor the runtime of TWS or Gateway.</b> It does not
restart them after a crash or session timeout, and it does not manage the connection
to the IB servers.</p>

<p>For automatic session management use the built-in <b>Auto Restart</b> feature of TWS:<br>
&nbsp;&nbsp;<i>TWS → Settings → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>Adding a Connection</h3>
<p>Click <b>+ Add Connection</b>. Enter a name, your IBKR username, password,
and select <b>Live</b> or <b>Paper Trading</b> mode. Paths are optional — leave
blank to use the defaults from Settings.</p>

<h3>Starting TWS / Gateway</h3>
<p>Click <b>[TWS]</b> to launch Trader WorkStation or <b>[Gateway]</b> to launch
IB Gateway. The login dialog opens and your credentials are filled in automatically.</p>
<p><i>Keep the login window visible and do not move the mouse while autofill is running.</i></p>

<h3>Multiple Versions</h3>
<p>Create one connection entry per TWS or Gateway installation and set the
<b>individual path</b> on each entry. This lets you run different TWS versions
(e.g. stable vs. latest) from one place.</p>

<h3>Status Indicators</h3>
<p>
<span style="color:#334155">●</span> Grey = stopped &nbsp;
<span style="color:#f59e0b">●</span> Yellow = starting &nbsp;
<span style="color:#22c55e">●</span> Green = running
</p>

<h3>Settings</h3>
<p>Set the default installation directories for TWS (default: <code>C:\\jts</code>)
and IB Gateway. Individual connections can override these paths.</p>

<h3>Security</h3>
<p>Passwords are encrypted with AES-256 (Fernet / PBKDF2) using a key derived
from your machine's hardware identifiers. The data file
(<code>~/.twsstarter/data.json</code>) cannot be decrypted on another computer.</p>
""",

'de': """
<h2>TWSStarter</h2>
<p>TWSStarter ist ein <b>Starter</b> für die Interactive Brokers
<b>Trader WorkStation (TWS)</b> und den <b>IB Gateway</b>. Der einzige Zweck
der Anwendung ist es, TWS oder Gateway komfortabel zu starten — auch in
verschiedenen Versionen gleichzeitig — und die Anmeldedaten automatisch
einzutragen.</p>

<p><b>TWSStarter überwacht die Laufzeit von TWS oder Gateway nicht.</b>
Die Anwendung startet TWS nach einem Absturz oder Session-Timeout nicht neu
und verwaltet auch keine Verbindung zu den IB-Servern.</p>

<p>Für automatisches Session-Management nutzen Sie das eingebaute
<b>Auto Restart</b>-Feature der TWS:<br>
&nbsp;&nbsp;<i>TWS → Einstellungen → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>Verbindung hinzufügen</h3>
<p>Klicken Sie auf <b>+ Verbindung hinzufügen</b>. Geben Sie einen Namen, Ihren
IBKR-Benutzernamen, Ihr Passwort ein und wählen Sie den Modus <b>Live</b> oder
<b>Paper Trading</b>. Pfade sind optional — leer lassen = globale Einstellung.</p>

<h3>TWS / Gateway starten</h3>
<p>Klicken Sie auf <b>[TWS]</b> oder <b>[Gateway]</b>. Der Login-Dialog öffnet
sich und Ihre Anmeldedaten werden automatisch eingetragen.</p>
<p><i>Halten Sie das Login-Fenster sichtbar und bewegen Sie die Maus nicht während
des Ausfüllens.</i></p>

<h3>Mehrere Versionen</h3>
<p>Legen Sie je einen Verbindungs-Eintrag pro TWS- oder Gateway-Installation an
und setzen Sie den <b>individuellen Pfad</b> pro Eintrag. So können Sie
verschiedene TWS-Versionen (z. B. Stable und Latest) bequem nebeneinander starten.</p>

<h3>Statusanzeige</h3>
<p>
<span style="color:#334155">●</span> Grau = gestoppt &nbsp;
<span style="color:#f59e0b">●</span> Gelb = startet &nbsp;
<span style="color:#22c55e">●</span> Grün = läuft
</p>

<h3>Einstellungen</h3>
<p>Legen Sie die Standard-Installationspfade für TWS (Standard: <code>C:\\jts</code>)
und IB Gateway fest. Einzelne Verbindungen können diese Pfade überschreiben.</p>

<h3>Sicherheit</h3>
<p>Passwörter werden mit AES-256 (Fernet / PBKDF2) verschlüsselt. Der Schlüssel
wird aus Hardware-Merkmalen Ihres Rechners abgeleitet. Die Datendatei
(<code>~/.twsstarter/data.json</code>) kann auf einem anderen Computer nicht
entschlüsselt werden.</p>
""",

'fr': """
<h2>TWSStarter</h2>
<p>TWSStarter est un <b>lanceur</b> pour <b>Trader WorkStation (TWS)</b> et
<b>IB Gateway</b> d'Interactive Brokers. Son unique but est de démarrer TWS ou
Gateway facilement — y compris plusieurs versions en parallèle — et de remplir
automatiquement les identifiants de connexion.</p>

<p><b>TWSStarter ne surveille pas l'exécution de TWS ou Gateway.</b> Il ne les
redémarre pas après un crash et ne gère pas la connexion aux serveurs IB.</p>

<p>Pour la gestion automatique de session, utilisez la fonction <b>Auto Restart</b>
de TWS :<br>
&nbsp;&nbsp;<i>TWS → Paramètres → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>Ajouter une connexion</h3>
<p>Cliquez sur <b>+ Ajouter une connexion</b>. Entrez un nom, votre identifiant
IBKR, votre mot de passe et sélectionnez le mode <b>Live</b> ou <b>Paper Trading</b>.</p>

<h3>Démarrer TWS / Gateway</h3>
<p>Cliquez sur <b>[TWS]</b> ou <b>[Gateway]</b>. La boîte de connexion s'ouvre et
vos identifiants sont remplis automatiquement.</p>
<p><i>Gardez la fenêtre de connexion visible et ne bougez pas la souris pendant le
remplissage automatique.</i></p>

<h3>Plusieurs versions</h3>
<p>Créez une entrée par installation TWS ou Gateway et définissez le
<b>chemin individuel</b> de chaque entrée pour gérer plusieurs versions côte à côte.</p>

<h3>Indicateurs de statut</h3>
<p>
<span style="color:#334155">●</span> Gris = arrêté &nbsp;
<span style="color:#f59e0b">●</span> Jaune = en démarrage &nbsp;
<span style="color:#22c55e">●</span> Vert = en cours
</p>

<h3>Paramètres</h3>
<p>Définissez les répertoires par défaut pour TWS (défaut : <code>C:\\jts</code>)
et IB Gateway.</p>

<h3>Sécurité</h3>
<p>Les mots de passe sont chiffrés AES-256 avec une clé dérivée des identifiants
matériels. Stockés dans <code>~/.twsstarter/data.json</code>.</p>
""",

'es': """
<h2>TWSStarter</h2>
<p>TWSStarter es un <b>lanzador</b> para <b>Trader WorkStation (TWS)</b> e
<b>IB Gateway</b> de Interactive Brokers. Su único propósito es iniciar TWS o
Gateway cómodamente — incluso varias versiones en paralelo — y rellenar las
credenciales de acceso automáticamente.</p>

<p><b>TWSStarter no supervisa el tiempo de ejecución de TWS o Gateway.</b>
No los reinicia tras un fallo y no gestiona la conexión con los servidores de IB.</p>

<p>Para la gestión automática de sesión use la función <b>Auto Restart</b> de TWS:<br>
&nbsp;&nbsp;<i>TWS → Configuración → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>Agregar una conexión</h3>
<p>Haga clic en <b>+ Agregar conexión</b>. Ingrese nombre, usuario IBKR, contraseña
y seleccione modo <b>Live</b> o <b>Paper Trading</b>.</p>

<h3>Iniciar TWS / Gateway</h3>
<p>Haga clic en <b>[TWS]</b> o <b>[Gateway]</b>. El diálogo se abre y las
credenciales se rellenan automáticamente.</p>
<p><i>Mantenga la ventana visible y no mueva el ratón durante el relleno automático.</i></p>

<h3>Varias versiones</h3>
<p>Cree una entrada por instalación y asigne una <b>ruta individual</b> para
gestionar distintas versiones de TWS o Gateway.</p>

<h3>Indicadores de estado</h3>
<p>
<span style="color:#334155">●</span> Gris = detenido &nbsp;
<span style="color:#f59e0b">●</span> Amarillo = iniciando &nbsp;
<span style="color:#22c55e">●</span> Verde = en ejecución
</p>

<h3>Configuración</h3>
<p>Rutas predeterminadas para TWS (predeterminado: <code>C:\\jts</code>) e IB Gateway.</p>

<h3>Seguridad</h3>
<p>Contraseñas cifradas AES-256 con clave de hardware.
Almacenadas en <code>~/.twsstarter/data.json</code>.</p>
""",

'it': """
<h2>TWSStarter</h2>
<p>TWSStarter è un <b>avviatore</b> per <b>Trader WorkStation (TWS)</b> e
<b>IB Gateway</b> di Interactive Brokers. Il suo unico scopo è avviare TWS o
Gateway comodamente — anche in versioni diverse in parallelo — e inserire
automaticamente le credenziali di accesso.</p>

<p><b>TWSStarter non monitora il tempo di esecuzione di TWS o Gateway.</b>
Non li riavvia dopo un crash e non gestisce la connessione ai server IB.</p>

<p>Per la gestione automatica della sessione usare la funzione <b>Auto Restart</b>
di TWS:<br>
&nbsp;&nbsp;<i>TWS → Impostazioni → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>Aggiungere una connessione</h3>
<p>Fare clic su <b>+ Aggiungi connessione</b>. Inserire nome, utente IBKR, password
e selezionare la modalità <b>Live</b> o <b>Paper Trading</b>.</p>

<h3>Avviare TWS / Gateway</h3>
<p>Fare clic su <b>[TWS]</b> o <b>[Gateway]</b>. La finestra di accesso si apre e
le credenziali vengono inserite automaticamente.</p>
<p><i>Mantenere la finestra visibile e non muovere il mouse durante la compilazione.</i></p>

<h3>Versioni multiple</h3>
<p>Creare un'entrata per ogni installazione con un <b>percorso individuale</b>
per gestire diverse versioni di TWS o Gateway.</p>

<h3>Indicatori di stato</h3>
<p>
<span style="color:#334155">●</span> Grigio = arrestato &nbsp;
<span style="color:#f59e0b">●</span> Giallo = avvio &nbsp;
<span style="color:#22c55e">●</span> Verde = in esecuzione
</p>

<h3>Impostazioni</h3>
<p>Percorsi predefiniti per TWS (predefinito: <code>C:\\jts</code>) e IB Gateway.</p>

<h3>Sicurezza</h3>
<p>Password crittografate AES-256 con chiave hardware.
Salvate in <code>~/.twsstarter/data.json</code>.</p>
""",

'pl': """
<h2>TWSStarter</h2>
<p>TWSStarter jest <b>uruchamiaczem</b> dla <b>Trader WorkStation (TWS)</b>
i <b>IB Gateway</b> firmy Interactive Brokers. Jego jedynym celem jest wygodne
uruchamianie TWS lub Gateway — także w wielu wersjach równolegle — oraz
automatyczne wypełnianie danych logowania.</p>

<p><b>TWSStarter nie monitoruje czasu działania TWS ani Gateway.</b>
Nie restartuje ich po awarii i nie zarządza połączeniem z serwerami IB.</p>

<p>Do automatycznego zarządzania sesją użyj funkcji <b>Auto Restart</b> TWS:<br>
&nbsp;&nbsp;<i>TWS → Ustawienia → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>Dodawanie połączenia</h3>
<p>Kliknij <b>+ Dodaj połączenie</b>. Wprowadź nazwę, użytkownika IBKR, hasło
i wybierz tryb <b>Live</b> lub <b>Paper Trading</b>.</p>

<h3>Uruchamianie TWS / Gateway</h3>
<p>Kliknij <b>[TWS]</b> lub <b>[Gateway]</b>. Okno logowania otworzy się
i dane zostaną wypełnione automatycznie.</p>
<p><i>Nie zasłaniaj okna logowania i nie ruszaj myszką podczas autouzupełniania.</i></p>

<h3>Wiele wersji</h3>
<p>Utwórz oddzielny wpis dla każdej instalacji i przypisz <b>indywidualną ścieżkę</b>,
aby zarządzać różnymi wersjami TWS lub Gateway.</p>

<h3>Wskaźniki statusu</h3>
<p>
<span style="color:#334155">●</span> Szary = zatrzymany &nbsp;
<span style="color:#f59e0b">●</span> Żółty = uruchamianie &nbsp;
<span style="color:#22c55e">●</span> Zielony = działa
</p>

<h3>Ustawienia</h3>
<p>Domyślne ścieżki dla TWS (domyślnie: <code>C:\\jts</code>) i IB Gateway.</p>

<h3>Bezpieczeństwo</h3>
<p>Hasła szyfrowane AES-256 kluczem sprzętowym.
Przechowywane w <code>~/.twsstarter/data.json</code>.</p>
""",

'tr': """
<h2>TWSStarter</h2>
<p>TWSStarter, Interactive Brokers <b>Trader WorkStation (TWS)</b> ve
<b>IB Gateway</b> için bir <b>başlatıcıdır</b>. Tek amacı TWS veya Gateway'i
rahatça başlatmak — birden fazla sürümü yan yana dahil — ve giriş bilgilerini
otomatik olarak doldurmaktır.</p>

<p><b>TWSStarter, TWS veya Gateway'in çalışma süresini izlemez.</b>
Kilitlenme sonrası yeniden başlatmaz ve IB sunucularıyla bağlantıyı yönetmez.</p>

<p>Otomatik oturum yönetimi için TWS'nin yerleşik <b>Auto Restart</b> özelliğini
kullanın:<br>
&nbsp;&nbsp;<i>TWS → Ayarlar → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>Bağlantı Ekleme</h3>
<p><b>+ Bağlantı Ekle</b>'ye tıklayın. Ad, IBKR kullanıcı adı, şifre girin ve
<b>Live</b> ya da <b>Paper Trading</b> modunu seçin.</p>

<h3>TWS / Gateway Başlatma</h3>
<p><b>[TWS]</b> veya <b>[Gateway]</b>'e tıklayın. Giriş penceresi açılır ve
kimlik bilgileri otomatik olarak doldurulur.</p>
<p><i>Otomatik doldurma sırasında giriş penceresini görünür tutun ve fareyi
hareket ettirmeyin.</i></p>

<h3>Birden Fazla Sürüm</h3>
<p>Her TWS veya Gateway kurulumu için ayrı bir giriş oluşturun ve her birine
<b>bireysel yol</b> atayarak farklı sürümleri yan yana yönetin.</p>

<h3>Durum Göstergeleri</h3>
<p>
<span style="color:#334155">●</span> Gri = durduruldu &nbsp;
<span style="color:#f59e0b">●</span> Sarı = başlatılıyor &nbsp;
<span style="color:#22c55e">●</span> Yeşil = çalışıyor
</p>

<h3>Ayarlar</h3>
<p>TWS (varsayılan: <code>C:\\jts</code>) ve IB Gateway için varsayılan dizinler.</p>

<h3>Güvenlik</h3>
<p>Şifreler donanım tabanlı AES-256 ile şifrelenir.
<code>~/.twsstarter/data.json</code> dosyasında saklanır.</p>
""",

'pt': """
<h2>TWSStarter</h2>
<p>TWSStarter é um <b>lançador</b> para o <b>Trader WorkStation (TWS)</b> e o
<b>IB Gateway</b> da Interactive Brokers. Seu único propósito é iniciar o TWS ou
Gateway de forma prática — inclusive múltiplas versões em paralelo — e preencher
as credenciais de acesso automaticamente.</p>

<p><b>TWSStarter não monitora o tempo de execução do TWS ou Gateway.</b>
Não os reinicia após uma falha e não gerencia a conexão com os servidores da IB.</p>

<p>Para gerenciamento automático de sessão use o recurso <b>Auto Restart</b> do TWS:<br>
&nbsp;&nbsp;<i>TWS → Configurações → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>Adicionar uma Conexão</h3>
<p>Clique em <b>+ Adicionar conexão</b>. Digite nome, usuário IBKR, senha e
selecione o modo <b>Live</b> ou <b>Paper Trading</b>.</p>

<h3>Iniciar TWS / Gateway</h3>
<p>Clique em <b>[TWS]</b> ou <b>[Gateway]</b>. A janela de login abrirá e as
credenciais serão preenchidas automaticamente.</p>
<p><i>Mantenha a janela visível e não mova o mouse durante o preenchimento.</i></p>

<h3>Múltiplas Versões</h3>
<p>Crie uma entrada por instalação com um <b>caminho individual</b> para gerenciar
diferentes versões do TWS ou Gateway.</p>

<h3>Indicadores de Status</h3>
<p>
<span style="color:#334155">●</span> Cinza = parado &nbsp;
<span style="color:#f59e0b">●</span> Amarelo = iniciando &nbsp;
<span style="color:#22c55e">●</span> Verde = em execução
</p>

<h3>Configurações</h3>
<p>Diretórios padrão para TWS (padrão: <code>C:\\jts</code>) e IB Gateway.</p>

<h3>Segurança</h3>
<p>Senhas criptografadas com AES-256 por chave de hardware.
Armazenadas em <code>~/.twsstarter/data.json</code>.</p>
""",

'ja': """
<h2>TWSStarter</h2>
<p>TWSStarter は Interactive Brokers の <b>Trader WorkStation (TWS)</b> および
<b>IB Gateway</b> 用の<b>起動ツール</b>です。唯一の目的は、TWS または
Gateway を手軽に起動すること — 複数バージョンの同時管理も含む — および
ログイン情報を自動入力することです。</p>

<p><b>TWSStarter は TWS や Gateway の稼働時間を監視しません。</b>
クラッシュ後の再起動も行わず、IB サーバーへの接続管理も行いません。</p>

<p>自動セッション管理には TWS の組み込み機能 <b>Auto Restart</b> を使用してください：<br>
&nbsp;&nbsp;<i>TWS → 設定 → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>接続の追加</h3>
<p><b>+ 接続を追加</b>をクリックし、名前・IBKRユーザー名・パスワードを入力して
<b>ライブ</b>または<b>ペーパー取引</b>モードを選択します。</p>

<h3>TWS / ゲートウェイの起動</h3>
<p><b>[TWS]</b> または <b>[Gateway]</b> をクリックするとログインダイアログが開き、
認証情報が自動的に入力されます。</p>
<p><i>自動入力中はログインウィンドウを表示させたまま、マウスを動かさないでください。</i></p>

<h3>複数バージョンの管理</h3>
<p>インストールごとに接続エントリを作成し、<b>個別パス</b>を設定することで
異なる TWS バージョンを並べて管理できます。</p>

<h3>ステータスインジケーター</h3>
<p>
<span style="color:#334155">●</span> グレー = 停止 &nbsp;
<span style="color:#f59e0b">●</span> 黄色 = 起動中 &nbsp;
<span style="color:#22c55e">●</span> 緑 = 実行中
</p>

<h3>設定</h3>
<p>TWS（デフォルト: <code>C:\\jts</code>）と IB Gateway のデフォルトディレクトリを設定します。</p>

<h3>セキュリティ</h3>
<p>パスワードはハードウェアキーによる AES-256 で暗号化されます。
<code>~/.twsstarter/data.json</code> に保存されます。</p>
""",

'zh': """
<h2>TWSStarter</h2>
<p>TWSStarter 是 Interactive Brokers <b>Trader WorkStation (TWS)</b> 和
<b>IB Gateway</b> 的<b>启动工具</b>。其唯一目的是方便地启动 TWS 或 Gateway
——包括并行管理多个版本——并自动填写登录凭据。</p>

<p><b>TWSStarter 不监控 TWS 或 Gateway 的运行状态。</b>
它不会在崩溃后重启，也不管理与 IB 服务器的连接。</p>

<p>如需自动会话管理，请使用 TWS 内置的 <b>Auto Restart</b> 功能：<br>
&nbsp;&nbsp;<i>TWS → 设置 → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>添加连接</h3>
<p>点击<b>+ 添加连接</b>，输入名称、IBKR 用户名、密码，并选择<b>实盘</b>
或<b>模拟交易</b>模式。</p>

<h3>启动 TWS / 网关</h3>
<p>点击<b>[TWS]</b>或<b>[Gateway]</b>，登录对话框将自动打开并填写凭据。</p>
<p><i>自动填写期间请保持登录窗口可见，不要移动鼠标。</i></p>

<h3>多版本管理</h3>
<p>为每个安装创建一个条目并设置<b>独立路径</b>，即可并排管理不同版本的 TWS 或 Gateway。</p>

<h3>状态指示器</h3>
<p>
<span style="color:#334155">●</span> 灰色 = 已停止 &nbsp;
<span style="color:#f59e0b">●</span> 黄色 = 启动中 &nbsp;
<span style="color:#22c55e">●</span> 绿色 = 运行中
</p>

<h3>设置</h3>
<p>TWS（默认: <code>C:\\jts</code>）和 IB Gateway 的默认目录。</p>

<h3>安全性</h3>
<p>密码使用基于硬件密钥的 AES-256 加密，存储于 <code>~/.twsstarter/data.json</code>。</p>
""",

'hi': """
<h2>TWSStarter</h2>
<p>TWSStarter, Interactive Brokers के <b>Trader WorkStation (TWS)</b> और
<b>IB Gateway</b> के लिए एक <b>लॉन्चर</b> है। इसका एकमात्र उद्देश्य TWS या
Gateway को आसानी से शुरू करना है — कई संस्करणों को एक साथ सहित — और
लॉगिन क्रेडेंशियल स्वचालित रूप से भरना है।</p>

<p><b>TWSStarter TWS या Gateway के रनटाइम की निगरानी नहीं करता।</b>
यह क्रैश के बाद पुनः आरंभ नहीं करता और IB सर्वर से कनेक्शन प्रबंधित नहीं करता।</p>

<p>स्वचालित सत्र प्रबंधन के लिए TWS की अंतर्निहित <b>Auto Restart</b> सुविधा
का उपयोग करें:<br>
&nbsp;&nbsp;<i>TWS → Settings → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>कनेक्शन जोड़ें</h3>
<p><b>+ कनेक्शन जोड़ें</b> पर क्लिक करें। नाम, IBKR उपयोगकर्ता नाम, पासवर्ड
दर्ज करें और <b>Live</b> या <b>Paper Trading</b> मोड चुनें।</p>

<h3>TWS / Gateway शुरू करें</h3>
<p><b>[TWS]</b> या <b>[Gateway]</b> पर क्लिक करें। लॉगिन डायलॉग खुलेगा
और क्रेडेंशियल स्वचालित रूप से भरे जाएंगे।</p>
<p><i>ऑटोफिल के दौरान लॉगिन विंडो दृश्यमान रखें और माउस न हिलाएं।</i></p>

<h3>कई संस्करण</h3>
<p>प्रत्येक इंस्टॉलेशन के लिए एक अलग प्रविष्टि बनाएं और <b>व्यक्तिगत पथ</b>
सेट करें ताकि विभिन्न TWS संस्करण एक साथ प्रबंधित हो सकें।</p>

<h3>स्थिति संकेतक</h3>
<p>
<span style="color:#334155">●</span> ग्रे = रुका हुआ &nbsp;
<span style="color:#f59e0b">●</span> पीला = शुरू हो रहा है &nbsp;
<span style="color:#22c55e">●</span> हरा = चल रहा है
</p>

<h3>सेटिंग्स</h3>
<p>TWS (डिफ़ॉल्ट: <code>C:\\jts</code>) और IB Gateway के लिए डिफ़ॉल्ट डायरेक्टरी।</p>

<h3>सुरक्षा</h3>
<p>पासवर्ड हार्डवेयर-आधारित AES-256 से एन्क्रिप्ट।
<code>~/.twsstarter/data.json</code> में संग्रहीत।</p>
""",

'ru': """
<h2>TWSStarter</h2>
<p>TWSStarter — это <b>лаунчер</b> для <b>Trader WorkStation (TWS)</b> и
<b>IB Gateway</b> от Interactive Brokers. Единственная цель приложения —
удобно запускать TWS или Gateway, в том числе несколько версий параллельно,
и автоматически вводить учётные данные.</p>

<p><b>TWSStarter не отслеживает время работы TWS или Gateway.</b>
Он не перезапускает их после сбоя и не управляет подключением к серверам IB.</p>

<p>Для автоматического управления сессией используйте встроенную функцию TWS
<b>Auto Restart</b>:<br>
&nbsp;&nbsp;<i>TWS → Настройки → Lock and Exit → Auto Restart</i></p>

<hr>

<h3>Добавление подключения</h3>
<p>Нажмите <b>+ Добавить соединение</b>. Введите имя, логин IBKR, пароль и
выберите режим <b>Live</b> или <b>Paper Trading</b>.</p>

<h3>Запуск TWS / Gateway</h3>
<p>Нажмите <b>[TWS]</b> или <b>[Gateway]</b>. Откроется диалог входа и учётные
данные будут введены автоматически.</p>
<p><i>Не закрывайте окно входа и не перемещайте мышь во время автозаполнения.</i></p>

<h3>Несколько версий</h3>
<p>Создайте отдельную запись для каждой установки и назначьте
<b>индивидуальный путь</b>, чтобы управлять разными версиями TWS или Gateway.</p>

<h3>Индикаторы состояния</h3>
<p>
<span style="color:#334155">●</span> Серый = остановлен &nbsp;
<span style="color:#f59e0b">●</span> Жёлтый = запускается &nbsp;
<span style="color:#22c55e">●</span> Зелёный = работает
</p>

<h3>Настройки</h3>
<p>Пути по умолчанию для TWS (по умолчанию: <code>C:\\jts</code>) и IB Gateway.</p>

<h3>Безопасность</h3>
<p>Пароли шифруются AES-256 с аппаратным ключом.
Хранятся в <code>~/.twsstarter/data.json</code>.</p>
""",
}

# ── UI Strings ─────────────────────────────────────────────────────────────

STRINGS: dict[str, dict[str, str]] = {

'en': {
    'subtitle':         'Interactive Brokers TWS / Gateway Launcher',
    'btn_settings':     '⚙  Settings',
    'btn_add':          '＋  Add Connection',
    'status_ready':     'Ready',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Stop',
    'btn_edit':         'Edit',
    'btn_delete':       'Delete',
    'tooltip_tws':      'Start TWS',
    'tooltip_gw':       'Start Gateway',
    'tooltip_stop':     'Stop instance',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(default)',
    'empty_state':      "No connections yet.\nClick '＋ Add Connection'.",
    'dlg_add_title':    'New Entry',
    'dlg_edit_title':   'Edit Entry',
    'dlg_heading_new':  'Connection',
    'dlg_heading_edit': 'Edit Connection',
    'lbl_name':         'Name',
    'lbl_username':     'Username',
    'lbl_password':     'Password',
    'lbl_mode':         'Trading Mode',
    'mode_live':        'Live Trading',
    'mode_paper':       'Paper Trading',
    'lbl_tws_path':     'TWS Path',
    'lbl_gw_path':      'Gateway Path',
    'hint_paths':       'Optional: individual paths for this entry. Leave blank to use global defaults.',
    'ph_name':          'e.g.  Paper Trader  or  Live Account',
    'ph_username':      'IBKR username / account ID',
    'ph_password':      'Password',
    'ph_pw_unchanged':  'Leave blank = keep current password',
    'btn_save':         'Save',
    'btn_cancel':       'Cancel',
    'settings_title':   'Settings',
    'section_paths':    'Default Paths',
    'lbl_tws_dir':      'TWS Directory',
    'lbl_gw_dir':       'Gateway Directory',
    'section_language': 'Language',
    'lbl_language':     'Language',
    'lang_restart':     'Restart required to apply language change.',
    'msg_added':        "'{name}' added.",
    'msg_updated':      "'{name}' updated.",
    'msg_deleted':      "'{name}' deleted.",
    'msg_starting':     "Starting {kind} for '{name}' …",
    'msg_started':      "{kind} for '{name}' started (PID {pid}).",
    'msg_start_err':    'Failed to start.',
    'msg_stopped':      "'{name}' stopped.",
    'msg_settings_ok':  'Settings saved.',
    'err_already_run':  "'{name}' is already running (PID {pid}).",
    'err_del_running':  "'{name}' is running.\nStop it before deleting.",
    'dlg_delete_title': 'Delete Entry',
    'dlg_delete_msg':   "Really delete '{name}'?",
    'dlg_active_title': 'Active Connections',
    'dlg_active_body':  '{count} connection(s) still running:',
    'dlg_active_quit':  'Exit anyway?',
    'menu_help':        'Help',
    'action_help':      'Help',
    'action_about':     'About',
    'about_title':      'About TWSStarter',
    'about_version':    'Version',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'IBKR TWS / Gateway Launcher with automatic login',
    'help_title':       'TWSStarter — Help',
    'help_text':        _HELP['en'],
},

'de': {
    'subtitle':         'Interactive Brokers TWS / Gateway Starter',
    'btn_settings':     '⚙  Einstellungen',
    'btn_add':          '＋  Verbindung hinzufügen',
    'status_ready':     'Bereit',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Stop',
    'btn_edit':         'Edit',
    'btn_delete':       'Delete',
    'tooltip_tws':      'TWS starten',
    'tooltip_gw':       'Gateway starten',
    'tooltip_stop':     'Instanz beenden',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(Standard)',
    'empty_state':      "Noch keine Verbindungen.\nKlicke auf '＋ Verbindung hinzufügen'.",
    'dlg_add_title':    'Neuer Eintrag',
    'dlg_edit_title':   'Eintrag bearbeiten',
    'dlg_heading_new':  'Verbindung',
    'dlg_heading_edit': 'Verbindung bearbeiten',
    'lbl_name':         'Bezeichnung',
    'lbl_username':     'Benutzername',
    'lbl_password':     'Passwort',
    'lbl_mode':         'Handelsmodus',
    'mode_live':        'Live Trading',
    'mode_paper':       'Paper Trading',
    'lbl_tws_path':     'TWS-Pfad',
    'lbl_gw_path':      'Gateway-Pfad',
    'hint_paths':       'Optional: individuelle Pfade für diesen Eintrag. Leer = globale Einstellung.',
    'ph_name':          'z. B.  Paper-Trader  oder  Live-Account',
    'ph_username':      'IBKR Benutzername / Account-ID',
    'ph_password':      'Passwort',
    'ph_pw_unchanged':  'Leer lassen = Passwort unverändert',
    'btn_save':         'Speichern',
    'btn_cancel':       'Abbrechen',
    'settings_title':   'Einstellungen',
    'section_paths':    'Standard-Pfade',
    'lbl_tws_dir':      'TWS-Verzeichnis',
    'lbl_gw_dir':       'Gateway-Verzeichnis',
    'section_language': 'Sprache',
    'lbl_language':     'Sprache',
    'lang_restart':     'Neustart erforderlich, um die Sprachänderung zu übernehmen.',
    'msg_added':        "'{name}' hinzugefügt.",
    'msg_updated':      "'{name}' aktualisiert.",
    'msg_deleted':      "'{name}' gelöscht.",
    'msg_starting':     "{kind} für '{name}' wird gestartet …",
    'msg_started':      "{kind} für '{name}' gestartet (PID {pid}).",
    'msg_start_err':    'Fehler beim Starten.',
    'msg_stopped':      "'{name}' gestoppt.",
    'msg_settings_ok':  'Einstellungen gespeichert.',
    'err_already_run':  "'{name}' läuft bereits (PID {pid}).",
    'err_del_running':  "'{name}' läuft gerade.\nBitte zuerst stoppen.",
    'dlg_delete_title': 'Eintrag löschen',
    'dlg_delete_msg':   "'{name}' wirklich löschen?",
    'dlg_active_title': 'Aktive Verbindungen',
    'dlg_active_body':  '{count} Verbindung(en) laufen noch:',
    'dlg_active_quit':  'Trotzdem beenden?',
    'menu_help':        'Hilfe',
    'action_help':      'Hilfe',
    'action_about':     'Über',
    'about_title':      'Über TWSStarter',
    'about_version':    'Version',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'IBKR TWS / Gateway Starter mit automatischem Login',
    'help_title':       'TWSStarter — Hilfe',
    'help_text':        _HELP['de'],
},

'fr': {
    'subtitle':         'Lanceur TWS / Gateway Interactive Brokers',
    'btn_settings':     '⚙  Paramètres',
    'btn_add':          '＋  Ajouter une connexion',
    'status_ready':     'Prêt',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Arrêter',
    'btn_edit':         'Modifier',
    'btn_delete':       'Supprimer',
    'tooltip_tws':      'Démarrer TWS',
    'tooltip_gw':       'Démarrer Gateway',
    'tooltip_stop':     "Arrêter l'instance",
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(défaut)',
    'empty_state':      "Aucune connexion.\nCliquez sur '＋ Ajouter une connexion'.",
    'dlg_add_title':    'Nouvelle entrée',
    'dlg_edit_title':   "Modifier l'entrée",
    'dlg_heading_new':  'Connexion',
    'dlg_heading_edit': 'Modifier la connexion',
    'lbl_name':         'Nom',
    'lbl_username':     "Nom d'utilisateur",
    'lbl_password':     'Mot de passe',
    'lbl_mode':         'Mode de trading',
    'mode_live':        'Trading réel',
    'mode_paper':       'Trading papier',
    'lbl_tws_path':     'Chemin TWS',
    'lbl_gw_path':      'Chemin Gateway',
    'hint_paths':       'Facultatif : chemins individuels. Vide = paramètres globaux.',
    'ph_name':          'ex.  Paper Trader  ou  Live Account',
    'ph_username':      "Nom d'utilisateur / ID de compte IBKR",
    'ph_password':      'Mot de passe',
    'ph_pw_unchanged':  'Vide = mot de passe inchangé',
    'btn_save':         'Enregistrer',
    'btn_cancel':       'Annuler',
    'settings_title':   'Paramètres',
    'section_paths':    'Chemins par défaut',
    'lbl_tws_dir':      'Répertoire TWS',
    'lbl_gw_dir':       'Répertoire Gateway',
    'section_language': 'Langue',
    'lbl_language':     'Langue',
    'lang_restart':     'Redémarrage requis pour appliquer le changement de langue.',
    'msg_added':        "'{name}' ajouté.",
    'msg_updated':      "'{name}' mis à jour.",
    'msg_deleted':      "'{name}' supprimé.",
    'msg_starting':     "Démarrage de {kind} pour '{name}' …",
    'msg_started':      "{kind} pour '{name}' démarré (PID {pid}).",
    'msg_start_err':    'Échec du démarrage.',
    'msg_stopped':      "'{name}' arrêté.",
    'msg_settings_ok':  'Paramètres enregistrés.',
    'err_already_run':  "'{name}' est déjà en cours (PID {pid}).",
    'err_del_running':  "'{name}' est en cours.\nVeuillez l'arrêter d'abord.",
    'dlg_delete_title': "Supprimer l'entrée",
    'dlg_delete_msg':   "Supprimer '{name}' ?",
    'dlg_active_title': 'Connexions actives',
    'dlg_active_body':  '{count} connexion(s) encore actives :',
    'dlg_active_quit':  'Quitter quand même ?',
    'menu_help':        'Aide',
    'action_help':      'Aide',
    'action_about':     'À propos',
    'about_title':      'À propos de TWSStarter',
    'about_version':    'Version',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'Lanceur IBKR TWS / Gateway avec connexion automatique',
    'help_title':       'TWSStarter — Aide',
    'help_text':        _HELP['fr'],
},

'es': {
    'subtitle':         'Lanzador TWS / Gateway de Interactive Brokers',
    'btn_settings':     '⚙  Configuración',
    'btn_add':          '＋  Agregar conexión',
    'status_ready':     'Listo',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Detener',
    'btn_edit':         'Editar',
    'btn_delete':       'Eliminar',
    'tooltip_tws':      'Iniciar TWS',
    'tooltip_gw':       'Iniciar Gateway',
    'tooltip_stop':     'Detener instancia',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(predeterminado)',
    'empty_state':      "Sin conexiones.\nHaga clic en '＋ Agregar conexión'.",
    'dlg_add_title':    'Nueva entrada',
    'dlg_edit_title':   'Editar entrada',
    'dlg_heading_new':  'Conexión',
    'dlg_heading_edit': 'Editar conexión',
    'lbl_name':         'Nombre',
    'lbl_username':     'Usuario',
    'lbl_password':     'Contraseña',
    'lbl_mode':         'Modo de trading',
    'mode_live':        'Trading real',
    'mode_paper':       'Trading simulado',
    'lbl_tws_path':     'Ruta TWS',
    'lbl_gw_path':      'Ruta Gateway',
    'hint_paths':       'Opcional: rutas individuales. Vacío = configuración global.',
    'ph_name':          'ej.  Paper Trader  o  Live Account',
    'ph_username':      'Usuario / ID de cuenta IBKR',
    'ph_password':      'Contraseña',
    'ph_pw_unchanged':  'Vacío = contraseña sin cambios',
    'btn_save':         'Guardar',
    'btn_cancel':       'Cancelar',
    'settings_title':   'Configuración',
    'section_paths':    'Rutas predeterminadas',
    'lbl_tws_dir':      'Directorio TWS',
    'lbl_gw_dir':       'Directorio Gateway',
    'section_language': 'Idioma',
    'lbl_language':     'Idioma',
    'lang_restart':     'Se requiere reinicio para aplicar el cambio de idioma.',
    'msg_added':        "'{name}' agregado.",
    'msg_updated':      "'{name}' actualizado.",
    'msg_deleted':      "'{name}' eliminado.",
    'msg_starting':     "Iniciando {kind} para '{name}' …",
    'msg_started':      "{kind} para '{name}' iniciado (PID {pid}).",
    'msg_start_err':    'Error al iniciar.',
    'msg_stopped':      "'{name}' detenido.",
    'msg_settings_ok':  'Configuración guardada.',
    'err_already_run':  "'{name}' ya está en ejecución (PID {pid}).",
    'err_del_running':  "'{name}' está en ejecución.\nDeténgalo primero.",
    'dlg_delete_title': 'Eliminar entrada',
    'dlg_delete_msg':   "¿Eliminar '{name}'?",
    'dlg_active_title': 'Conexiones activas',
    'dlg_active_body':  '{count} conexión/es aún activa/s:',
    'dlg_active_quit':  '¿Salir de todas formas?',
    'menu_help':        'Ayuda',
    'action_help':      'Ayuda',
    'action_about':     'Acerca de',
    'about_title':      'Acerca de TWSStarter',
    'about_version':    'Versión',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'Lanzador IBKR TWS / Gateway con inicio de sesión automático',
    'help_title':       'TWSStarter — Ayuda',
    'help_text':        _HELP['es'],
},

'it': {
    'subtitle':         'Avviatore TWS / Gateway Interactive Brokers',
    'btn_settings':     '⚙  Impostazioni',
    'btn_add':          '＋  Aggiungi connessione',
    'status_ready':     'Pronto',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Ferma',
    'btn_edit':         'Modifica',
    'btn_delete':       'Elimina',
    'tooltip_tws':      'Avvia TWS',
    'tooltip_gw':       'Avvia Gateway',
    'tooltip_stop':     "Ferma l'istanza",
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(predefinito)',
    'empty_state':      "Nessuna connessione.\nFare clic su '＋ Aggiungi connessione'.",
    'dlg_add_title':    'Nuova voce',
    'dlg_edit_title':   'Modifica voce',
    'dlg_heading_new':  'Connessione',
    'dlg_heading_edit': 'Modifica connessione',
    'lbl_name':         'Nome',
    'lbl_username':     'Nome utente',
    'lbl_password':     'Password',
    'lbl_mode':         'Modalità di trading',
    'mode_live':        'Trading reale',
    'mode_paper':       'Trading simulato',
    'lbl_tws_path':     'Percorso TWS',
    'lbl_gw_path':      'Percorso Gateway',
    'hint_paths':       'Facoltativo: percorsi individuali. Vuoto = impostazioni globali.',
    'ph_name':          'es.  Paper Trader  o  Live Account',
    'ph_username':      'Nome utente / ID account IBKR',
    'ph_password':      'Password',
    'ph_pw_unchanged':  'Vuoto = password invariata',
    'btn_save':         'Salva',
    'btn_cancel':       'Annulla',
    'settings_title':   'Impostazioni',
    'section_paths':    'Percorsi predefiniti',
    'lbl_tws_dir':      'Directory TWS',
    'lbl_gw_dir':       'Directory Gateway',
    'section_language': 'Lingua',
    'lbl_language':     'Lingua',
    'lang_restart':     'Riavvio necessario per applicare il cambio di lingua.',
    'msg_added':        "'{name}' aggiunto.",
    'msg_updated':      "'{name}' aggiornato.",
    'msg_deleted':      "'{name}' eliminato.",
    'msg_starting':     "Avvio di {kind} per '{name}' …",
    'msg_started':      "{kind} per '{name}' avviato (PID {pid}).",
    'msg_start_err':    "Avvio non riuscito.",
    'msg_stopped':      "'{name}' fermato.",
    'msg_settings_ok':  'Impostazioni salvate.',
    'err_already_run':  "'{name}' è già in esecuzione (PID {pid}).",
    'err_del_running':  "'{name}' è in esecuzione.\nFermarlo prima.",
    'dlg_delete_title': 'Elimina voce',
    'dlg_delete_msg':   "Eliminare '{name}'?",
    'dlg_active_title': 'Connessioni attive',
    'dlg_active_body':  '{count} connessione/i ancora attiva/e:',
    'dlg_active_quit':  'Uscire comunque?',
    'menu_help':        'Guida',
    'action_help':      'Guida',
    'action_about':     'Informazioni',
    'about_title':      'Informazioni su TWSStarter',
    'about_version':    'Versione',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'Avviatore IBKR TWS / Gateway con login automatico',
    'help_title':       'TWSStarter — Guida',
    'help_text':        _HELP['it'],
},

'pl': {
    'subtitle':         'Uruchamiacz TWS / Gateway Interactive Brokers',
    'btn_settings':     '⚙  Ustawienia',
    'btn_add':          '＋  Dodaj połączenie',
    'status_ready':     'Gotowy',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Zatrzymaj',
    'btn_edit':         'Edytuj',
    'btn_delete':       'Usuń',
    'tooltip_tws':      'Uruchom TWS',
    'tooltip_gw':       'Uruchom Gateway',
    'tooltip_stop':     'Zatrzymaj instancję',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(domyślny)',
    'empty_state':      "Brak połączeń.\nKliknij '＋ Dodaj połączenie'.",
    'dlg_add_title':    'Nowy wpis',
    'dlg_edit_title':   'Edytuj wpis',
    'dlg_heading_new':  'Połączenie',
    'dlg_heading_edit': 'Edytuj połączenie',
    'lbl_name':         'Nazwa',
    'lbl_username':     'Nazwa użytkownika',
    'lbl_password':     'Hasło',
    'lbl_mode':         'Tryb handlu',
    'mode_live':        'Handel prawdziwy',
    'mode_paper':       'Handel symulowany',
    'lbl_tws_path':     'Ścieżka TWS',
    'lbl_gw_path':      'Ścieżka Gateway',
    'hint_paths':       'Opcjonalnie: indywidualne ścieżki. Puste = ustawienia globalne.',
    'ph_name':          'np.  Paper Trader  lub  Live Account',
    'ph_username':      'Nazwa użytkownika / ID konta IBKR',
    'ph_password':      'Hasło',
    'ph_pw_unchanged':  'Puste = hasło bez zmian',
    'btn_save':         'Zapisz',
    'btn_cancel':       'Anuluj',
    'settings_title':   'Ustawienia',
    'section_paths':    'Domyślne ścieżki',
    'lbl_tws_dir':      'Katalog TWS',
    'lbl_gw_dir':       'Katalog Gateway',
    'section_language': 'Język',
    'lbl_language':     'Język',
    'lang_restart':     'Wymagane ponowne uruchomienie po zmianie języka.',
    'msg_added':        "'{name}' dodano.",
    'msg_updated':      "'{name}' zaktualizowano.",
    'msg_deleted':      "'{name}' usunięto.",
    'msg_starting':     "Uruchamianie {kind} dla '{name}' …",
    'msg_started':      "{kind} dla '{name}' uruchomiony (PID {pid}).",
    'msg_start_err':    'Nie udało się uruchomić.',
    'msg_stopped':      "'{name}' zatrzymany.",
    'msg_settings_ok':  'Ustawienia zapisane.',
    'err_already_run':  "'{name}' już działa (PID {pid}).",
    'err_del_running':  "'{name}' działa.\nZatrzymaj go najpierw.",
    'dlg_delete_title': 'Usuń wpis',
    'dlg_delete_msg':   "Usunąć '{name}'?",
    'dlg_active_title': 'Aktywne połączenia',
    'dlg_active_body':  '{count} połączenie/a nadal aktywne:',
    'dlg_active_quit':  'Zamknąć mimo to?',
    'menu_help':        'Pomoc',
    'action_help':      'Pomoc',
    'action_about':     'O programie',
    'about_title':      'O programie TWSStarter',
    'about_version':    'Wersja',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'Uruchamiacz IBKR TWS / Gateway z automatycznym logowaniem',
    'help_title':       'TWSStarter — Pomoc',
    'help_text':        _HELP['pl'],
},

'tr': {
    'subtitle':         'Interactive Brokers TWS / Gateway Başlatıcı',
    'btn_settings':     '⚙  Ayarlar',
    'btn_add':          '＋  Bağlantı Ekle',
    'status_ready':     'Hazır',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Durdur',
    'btn_edit':         'Düzenle',
    'btn_delete':       'Sil',
    'tooltip_tws':      'TWS başlat',
    'tooltip_gw':       'Gateway başlat',
    'tooltip_stop':     'Örneği durdur',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(varsayılan)',
    'empty_state':      "Henüz bağlantı yok.\n'＋ Bağlantı Ekle'ye tıklayın.",
    'dlg_add_title':    'Yeni Giriş',
    'dlg_edit_title':   'Girişi Düzenle',
    'dlg_heading_new':  'Bağlantı',
    'dlg_heading_edit': 'Bağlantıyı Düzenle',
    'lbl_name':         'Ad',
    'lbl_username':     'Kullanıcı adı',
    'lbl_password':     'Şifre',
    'lbl_mode':         'İşlem modu',
    'mode_live':        'Gerçek işlem',
    'mode_paper':       'Kağıt işlem',
    'lbl_tws_path':     'TWS Yolu',
    'lbl_gw_path':      'Gateway Yolu',
    'hint_paths':       'İsteğe bağlı: bireysel yollar. Boş = genel ayarlar.',
    'ph_name':          'ör.  Kağıt İşlem  veya  Canlı Hesap',
    'ph_username':      'IBKR kullanıcı adı / hesap ID',
    'ph_password':      'Şifre',
    'ph_pw_unchanged':  'Boş = şifre değişmeden kalır',
    'btn_save':         'Kaydet',
    'btn_cancel':       'İptal',
    'settings_title':   'Ayarlar',
    'section_paths':    'Varsayılan Yollar',
    'lbl_tws_dir':      'TWS Dizini',
    'lbl_gw_dir':       'Gateway Dizini',
    'section_language': 'Dil',
    'lbl_language':     'Dil',
    'lang_restart':     'Dil değişikliği için yeniden başlatma gerekiyor.',
    'msg_added':        "'{name}' eklendi.",
    'msg_updated':      "'{name}' güncellendi.",
    'msg_deleted':      "'{name}' silindi.",
    'msg_starting':     "'{name}' için {kind} başlatılıyor …",
    'msg_started':      "'{name}' için {kind} başlatıldı (PID {pid}).",
    'msg_start_err':    'Başlatma başarısız.',
    'msg_stopped':      "'{name}' durduruldu.",
    'msg_settings_ok':  'Ayarlar kaydedildi.',
    'err_already_run':  "'{name}' zaten çalışıyor (PID {pid}).",
    'err_del_running':  "'{name}' çalışıyor.\nÖnce durdurun.",
    'dlg_delete_title': 'Girişi Sil',
    'dlg_delete_msg':   "'{name}' silinsin mi?",
    'dlg_active_title': 'Etkin Bağlantılar',
    'dlg_active_body':  '{count} bağlantı hâlâ aktif:',
    'dlg_active_quit':  'Yine de çıkılsın mı?',
    'menu_help':        'Yardım',
    'action_help':      'Yardım',
    'action_about':     'Hakkında',
    'about_title':      'TWSStarter Hakkında',
    'about_version':    'Sürüm',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'Otomatik girişli IBKR TWS / Gateway Başlatıcı',
    'help_title':       'TWSStarter — Yardım',
    'help_text':        _HELP['tr'],
},

'pt': {
    'subtitle':         'Lançador TWS / Gateway Interactive Brokers',
    'btn_settings':     '⚙  Configurações',
    'btn_add':          '＋  Adicionar conexão',
    'status_ready':     'Pronto',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Parar',
    'btn_edit':         'Editar',
    'btn_delete':       'Excluir',
    'tooltip_tws':      'Iniciar TWS',
    'tooltip_gw':       'Iniciar Gateway',
    'tooltip_stop':     'Parar instância',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(padrão)',
    'empty_state':      "Nenhuma conexão.\nClique em '＋ Adicionar conexão'.",
    'dlg_add_title':    'Nova entrada',
    'dlg_edit_title':   'Editar entrada',
    'dlg_heading_new':  'Conexão',
    'dlg_heading_edit': 'Editar conexão',
    'lbl_name':         'Nome',
    'lbl_username':     'Nome de usuário',
    'lbl_password':     'Senha',
    'lbl_mode':         'Modo de negociação',
    'mode_live':        'Negociação real',
    'mode_paper':       'Negociação simulada',
    'lbl_tws_path':     'Caminho TWS',
    'lbl_gw_path':      'Caminho Gateway',
    'hint_paths':       'Opcional: caminhos individuais. Vazio = configurações globais.',
    'ph_name':          'ex.  Paper Trader  ou  Live Account',
    'ph_username':      'Usuário / ID de conta IBKR',
    'ph_password':      'Senha',
    'ph_pw_unchanged':  'Vazio = senha inalterada',
    'btn_save':         'Salvar',
    'btn_cancel':       'Cancelar',
    'settings_title':   'Configurações',
    'section_paths':    'Caminhos padrão',
    'lbl_tws_dir':      'Diretório TWS',
    'lbl_gw_dir':       'Diretório Gateway',
    'section_language': 'Idioma',
    'lbl_language':     'Idioma',
    'lang_restart':     'Reinicialização necessária para aplicar a mudança de idioma.',
    'msg_added':        "'{name}' adicionado.",
    'msg_updated':      "'{name}' atualizado.",
    'msg_deleted':      "'{name}' excluído.",
    'msg_starting':     "Iniciando {kind} para '{name}' …",
    'msg_started':      "{kind} para '{name}' iniciado (PID {pid}).",
    'msg_start_err':    'Falha ao iniciar.',
    'msg_stopped':      "'{name}' parado.",
    'msg_settings_ok':  'Configurações salvas.',
    'err_already_run':  "'{name}' já está em execução (PID {pid}).",
    'err_del_running':  "'{name}' está em execução.\nPare-o primeiro.",
    'dlg_delete_title': 'Excluir entrada',
    'dlg_delete_msg':   "Excluir '{name}'?",
    'dlg_active_title': 'Conexões ativas',
    'dlg_active_body':  '{count} conexão/ões ainda ativa/s:',
    'dlg_active_quit':  'Sair mesmo assim?',
    'menu_help':        'Ajuda',
    'action_help':      'Ajuda',
    'action_about':     'Sobre',
    'about_title':      'Sobre o TWSStarter',
    'about_version':    'Versão',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'Lançador IBKR TWS / Gateway com login automático',
    'help_title':       'TWSStarter — Ajuda',
    'help_text':        _HELP['pt'],
},

'ja': {
    'subtitle':         'Interactive Brokers TWS / ゲートウェイ起動ツール',
    'btn_settings':     '⚙  設定',
    'btn_add':          '＋  接続を追加',
    'status_ready':     '準備完了',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         '停止',
    'btn_edit':         '編集',
    'btn_delete':       '削除',
    'tooltip_tws':      'TWS を起動',
    'tooltip_gw':       'Gateway を起動',
    'tooltip_stop':     'インスタンスを停止',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(デフォルト)',
    'empty_state':      "接続がありません。\n'＋ 接続を追加' をクリックしてください。",
    'dlg_add_title':    '新規エントリ',
    'dlg_edit_title':   'エントリを編集',
    'dlg_heading_new':  '接続',
    'dlg_heading_edit': '接続を編集',
    'lbl_name':         '名前',
    'lbl_username':     'ユーザー名',
    'lbl_password':     'パスワード',
    'lbl_mode':         '取引モード',
    'mode_live':        '本番取引',
    'mode_paper':       '模擬取引',
    'lbl_tws_path':     'TWS パス',
    'lbl_gw_path':      'Gateway パス',
    'hint_paths':       '任意: 個別パス。空白 = グローバル設定を使用。',
    'ph_name':          '例: ペーパートレーダー または ライブアカウント',
    'ph_username':      'IBKR ユーザー名 / アカウント ID',
    'ph_password':      'パスワード',
    'ph_pw_unchanged':  '空白 = パスワードを変更しない',
    'btn_save':         '保存',
    'btn_cancel':       'キャンセル',
    'settings_title':   '設定',
    'section_paths':    'デフォルトパス',
    'lbl_tws_dir':      'TWS ディレクトリ',
    'lbl_gw_dir':       'Gateway ディレクトリ',
    'section_language': '言語',
    'lbl_language':     '言語',
    'lang_restart':     '言語の変更を適用するには再起動が必要です。',
    'msg_added':        "'{name}' を追加しました。",
    'msg_updated':      "'{name}' を更新しました。",
    'msg_deleted':      "'{name}' を削除しました。",
    'msg_starting':     "'{name}' の {kind} を起動中 …",
    'msg_started':      "'{name}' の {kind} を起動しました (PID {pid})。",
    'msg_start_err':    '起動に失敗しました。',
    'msg_stopped':      "'{name}' を停止しました。",
    'msg_settings_ok':  '設定を保存しました。',
    'err_already_run':  "'{name}' はすでに実行中です (PID {pid})。",
    'err_del_running':  "'{name}' は実行中です。\nまず停止してください。",
    'dlg_delete_title': 'エントリを削除',
    'dlg_delete_msg':   "'{name}' を削除しますか？",
    'dlg_active_title': 'アクティブな接続',
    'dlg_active_body':  '{count} 件の接続がまだ実行中:',
    'dlg_active_quit':  'それでも終了しますか？',
    'menu_help':        'ヘルプ',
    'action_help':      'ヘルプ',
    'action_about':     'バージョン情報',
    'about_title':      'TWSStarter について',
    'about_version':    'バージョン',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       '自動ログイン付き IBKR TWS / Gateway 起動ツール',
    'help_title':       'TWSStarter — ヘルプ',
    'help_text':        _HELP['ja'],
},

'zh': {
    'subtitle':         '盈透证券 TWS / 网关启动工具',
    'btn_settings':     '⚙  设置',
    'btn_add':          '＋  添加连接',
    'status_ready':     '就绪',
    'btn_tws':          'TWS',
    'btn_gateway':      '网关',
    'btn_stop':         '停止',
    'btn_edit':         '编辑',
    'btn_delete':       '删除',
    'tooltip_tws':      '启动 TWS',
    'tooltip_gw':       '启动网关',
    'tooltip_stop':     '停止实例',
    'badge_live':       '实盘',
    'badge_paper':      '模拟',
    'path_default':     '(默认)',
    'empty_state':      "暂无连接。\n点击 '＋ 添加连接'。",
    'dlg_add_title':    '新建条目',
    'dlg_edit_title':   '编辑条目',
    'dlg_heading_new':  '连接',
    'dlg_heading_edit': '编辑连接',
    'lbl_name':         '名称',
    'lbl_username':     '用户名',
    'lbl_password':     '密码',
    'lbl_mode':         '交易模式',
    'mode_live':        '实盘交易',
    'mode_paper':       '模拟交易',
    'lbl_tws_path':     'TWS 路径',
    'lbl_gw_path':      '网关路径',
    'hint_paths':       '可选：单独路径。留空 = 使用全局设置。',
    'ph_name':          '例如：模拟账户 或 实盘账户',
    'ph_username':      'IBKR 用户名 / 账户 ID',
    'ph_password':      '密码',
    'ph_pw_unchanged':  '留空 = 密码不变',
    'btn_save':         '保存',
    'btn_cancel':       '取消',
    'settings_title':   '设置',
    'section_paths':    '默认路径',
    'lbl_tws_dir':      'TWS 目录',
    'lbl_gw_dir':       '网关目录',
    'section_language': '语言',
    'lbl_language':     '语言',
    'lang_restart':     '语言更改需要重启应用。',
    'msg_added':        "已添加 '{name}'。",
    'msg_updated':      "已更新 '{name}'。",
    'msg_deleted':      "已删除 '{name}'。",
    'msg_starting':     "正在为 '{name}' 启动 {kind} …",
    'msg_started':      "已为 '{name}' 启动 {kind}（PID {pid}）。",
    'msg_start_err':    '启动失败。',
    'msg_stopped':      "已停止 '{name}'。",
    'msg_settings_ok':  '设置已保存。',
    'err_already_run':  "'{name}' 已在运行中（PID {pid}）。",
    'err_del_running':  "'{name}' 正在运行。\n请先停止它。",
    'dlg_delete_title': '删除条目',
    'dlg_delete_msg':   "确定删除 '{name}'？",
    'dlg_active_title': '活跃连接',
    'dlg_active_body':  '{count} 个连接仍在运行：',
    'dlg_active_quit':  '仍然退出？',
    'menu_help':        '帮助',
    'action_help':      '帮助',
    'action_about':     '关于',
    'about_title':      '关于 TWSStarter',
    'about_version':    '版本',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       '带自动登录的 IBKR TWS / 网关启动工具',
    'help_title':       'TWSStarter — 帮助',
    'help_text':        _HELP['zh'],
},

'hi': {
    'subtitle':         'Interactive Brokers TWS / Gateway लॉन्चर',
    'btn_settings':     '⚙  सेटिंग्स',
    'btn_add':          '＋  कनेक्शन जोड़ें',
    'status_ready':     'तैयार',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'रोकें',
    'btn_edit':         'संपादित करें',
    'btn_delete':       'हटाएं',
    'tooltip_tws':      'TWS शुरू करें',
    'tooltip_gw':       'Gateway शुरू करें',
    'tooltip_stop':     'इंस्टेंस रोकें',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(डिफ़ॉल्ट)',
    'empty_state':      "कोई कनेक्शन नहीं।\n'＋ कनेक्शन जोड़ें' पर क्लिक करें।",
    'dlg_add_title':    'नई प्रविष्टि',
    'dlg_edit_title':   'प्रविष्टि संपादित करें',
    'dlg_heading_new':  'कनेक्शन',
    'dlg_heading_edit': 'कनेक्शन संपादित करें',
    'lbl_name':         'नाम',
    'lbl_username':     'उपयोगकर्ता नाम',
    'lbl_password':     'पासवर्ड',
    'lbl_mode':         'ट्रेडिंग मोड',
    'mode_live':        'लाइव ट्रेडिंग',
    'mode_paper':       'पेपर ट्रेडिंग',
    'lbl_tws_path':     'TWS पथ',
    'lbl_gw_path':      'Gateway पथ',
    'hint_paths':       'वैकल्पिक: व्यक्तिगत पथ। खाली = वैश्विक सेटिंग।',
    'ph_name':          'उदा.  पेपर ट्रेडर  या  लाइव अकाउंट',
    'ph_username':      'IBKR उपयोगकर्ता नाम / खाता ID',
    'ph_password':      'पासवर्ड',
    'ph_pw_unchanged':  'खाली = पासवर्ड अपरिवर्तित',
    'btn_save':         'सहेजें',
    'btn_cancel':       'रद्द करें',
    'settings_title':   'सेटिंग्स',
    'section_paths':    'डिफ़ॉल्ट पथ',
    'lbl_tws_dir':      'TWS डायरेक्टरी',
    'lbl_gw_dir':       'Gateway डायरेक्टरी',
    'section_language': 'भाषा',
    'lbl_language':     'भाषा',
    'lang_restart':     'भाषा परिवर्तन लागू करने के लिए पुनः आरंभ आवश्यक है।',
    'msg_added':        "'{name}' जोड़ा गया।",
    'msg_updated':      "'{name}' अपडेट किया गया।",
    'msg_deleted':      "'{name}' हटाया गया।",
    'msg_starting':     "'{name}' के लिए {kind} शुरू हो रहा है …",
    'msg_started':      "'{name}' के लिए {kind} शुरू हुआ (PID {pid})।",
    'msg_start_err':    'शुरू करने में विफल।',
    'msg_stopped':      "'{name}' रोका गया।",
    'msg_settings_ok':  'सेटिंग्स सहेजी गईं।',
    'err_already_run':  "'{name}' पहले से चल रहा है (PID {pid})।",
    'err_del_running':  "'{name}' चल रहा है।\nपहले इसे रोकें।",
    'dlg_delete_title': 'प्रविष्टि हटाएं',
    'dlg_delete_msg':   "'{name}' हटाएं?",
    'dlg_active_title': 'सक्रिय कनेक्शन',
    'dlg_active_body':  '{count} कनेक्शन अभी भी चल रहे हैं:',
    'dlg_active_quit':  'फिर भी बाहर निकलें?',
    'menu_help':        'सहायता',
    'action_help':      'सहायता',
    'action_about':     'के बारे में',
    'about_title':      'TWSStarter के बारे में',
    'about_version':    'संस्करण',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'स्वचालित लॉगिन के साथ IBKR TWS / Gateway लॉन्चर',
    'help_title':       'TWSStarter — सहायता',
    'help_text':        _HELP['hi'],
},

'ru': {
    'subtitle':         'Запуск TWS / Gateway Interactive Brokers',
    'btn_settings':     '⚙  Настройки',
    'btn_add':          '＋  Добавить соединение',
    'status_ready':     'Готово',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Стоп',
    'btn_edit':         'Изменить',
    'btn_delete':       'Удалить',
    'tooltip_tws':      'Запустить TWS',
    'tooltip_gw':       'Запустить Gateway',
    'tooltip_stop':     'Остановить экземпляр',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(по умолч.)',
    'empty_state':      "Нет соединений.\nНажмите '＋ Добавить соединение'.",
    'dlg_add_title':    'Новая запись',
    'dlg_edit_title':   'Редактировать запись',
    'dlg_heading_new':  'Соединение',
    'dlg_heading_edit': 'Редактировать соединение',
    'lbl_name':         'Название',
    'lbl_username':     'Имя пользователя',
    'lbl_password':     'Пароль',
    'lbl_mode':         'Режим торговли',
    'mode_live':        'Реальная торговля',
    'mode_paper':       'Бумажная торговля',
    'lbl_tws_path':     'Путь TWS',
    'lbl_gw_path':      'Путь Gateway',
    'hint_paths':       'Необязательно: индивидуальные пути. Пусто = глобальные настройки.',
    'ph_name':          'напр.  Бумажный трейдер  или  Реальный счёт',
    'ph_username':      'Имя пользователя / ID счёта IBKR',
    'ph_password':      'Пароль',
    'ph_pw_unchanged':  'Пусто = пароль без изменений',
    'btn_save':         'Сохранить',
    'btn_cancel':       'Отмена',
    'settings_title':   'Настройки',
    'section_paths':    'Пути по умолчанию',
    'lbl_tws_dir':      'Каталог TWS',
    'lbl_gw_dir':       'Каталог Gateway',
    'section_language': 'Язык',
    'lbl_language':     'Язык',
    'lang_restart':     'Для применения языка требуется перезапуск.',
    'msg_added':        "'{name}' добавлено.",
    'msg_updated':      "'{name}' обновлено.",
    'msg_deleted':      "'{name}' удалено.",
    'msg_starting':     "Запуск {kind} для '{name}' …",
    'msg_started':      "{kind} для '{name}' запущен (PID {pid}).",
    'msg_start_err':    'Ошибка запуска.',
    'msg_stopped':      "'{name}' остановлен.",
    'msg_settings_ok':  'Настройки сохранены.',
    'err_already_run':  "'{name}' уже запущен (PID {pid}).",
    'err_del_running':  "'{name}' запущен.\nСначала остановите его.",
    'dlg_delete_title': 'Удалить запись',
    'dlg_delete_msg':   "Удалить '{name}'?",
    'dlg_active_title': 'Активные соединения',
    'dlg_active_body':  'Ещё {count} соединение/ий активно:',
    'dlg_active_quit':  'Всё равно выйти?',
    'menu_help':        'Справка',
    'action_help':      'Справка',
    'action_about':     'О программе',
    'about_title':      'О программе TWSStarter',
    'about_version':    'Версия',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'Запуск IBKR TWS / Gateway с автоматическим входом',
    'help_title':       'TWSStarter — Справка',
    'help_text':        _HELP['ru'],
},

'nl': {
    'subtitle':         'Interactive Brokers TWS / Gateway Launcher',
    'btn_settings':     '⚙  Instellingen',
    'btn_add':          '＋  Verbinding toevoegen',
    'status_ready':     'Gereed',
    'btn_tws':          'TWS',
    'btn_gateway':      'Gateway',
    'btn_stop':         'Stoppen',
    'btn_edit':         'Bewerken',
    'btn_delete':       'Verwijderen',
    'tooltip_tws':      'TWS starten',
    'tooltip_gw':       'Gateway starten',
    'tooltip_stop':     'Instantie stoppen',
    'badge_live':       'LIVE',
    'badge_paper':      'PAPER',
    'path_default':     '(standaard)',
    'empty_state':      "Nog geen verbindingen.\nKlik op '＋ Verbinding toevoegen'.",
    'dlg_add_title':    'Nieuw item',
    'dlg_edit_title':   'Item bewerken',
    'dlg_heading_new':  'Verbinding',
    'dlg_heading_edit': 'Verbinding bewerken',
    'lbl_name':         'Naam',
    'lbl_username':     'Gebruikersnaam',
    'lbl_password':     'Wachtwoord',
    'lbl_mode':         'Handelsmodus',
    'mode_live':        'Live Trading',
    'mode_paper':       'Paper Trading',
    'lbl_tws_path':     'TWS-pad',
    'lbl_gw_path':      'Gateway-pad',
    'hint_paths':       'Optioneel: eigen paden voor dit item. Laat leeg om de globale standaarden te gebruiken.',
    'ph_name':          'bijv.  Paper Trader  of  Live-account',
    'ph_username':      'IBKR-gebruikersnaam / account-ID',
    'ph_password':      'Wachtwoord',
    'ph_pw_unchanged':  'Leeg laten = huidig wachtwoord behouden',
    'btn_save':         'Opslaan',
    'btn_cancel':       'Annuleren',
    'settings_title':   'Instellingen',
    'section_paths':    'Standaardpaden',
    'lbl_tws_dir':      'TWS-map',
    'lbl_gw_dir':       'Gateway-map',
    'section_language': 'Taal',
    'lbl_language':     'Taal',
    'lang_restart':     'Herstart vereist om de taalwijziging toe te passen.',
    'msg_added':        "'{name}' toegevoegd.",
    'msg_updated':      "'{name}' bijgewerkt.",
    'msg_deleted':      "'{name}' verwijderd.",
    'msg_starting':     "{kind} voor '{name}' starten …",
    'msg_started':      "{kind} voor '{name}' gestart (PID {pid}).",
    'msg_start_err':    'Starten mislukt.',
    'msg_stopped':      "'{name}' gestopt.",
    'msg_settings_ok':  'Instellingen opgeslagen.',
    'err_already_run':  "'{name}' draait al (PID {pid}).",
    'err_del_running':  "'{name}' draait.\nStop het voordat u verwijdert.",
    'dlg_delete_title': 'Item verwijderen',
    'dlg_delete_msg':   "'{name}' echt verwijderen?",
    'dlg_active_title': 'Actieve verbindingen',
    'dlg_active_body':  '{count} verbinding(en) draaien nog:',
    'dlg_active_quit':  'Toch afsluiten?',
    'menu_help':        'Help',
    'action_help':      'Help',
    'action_about':     'Over',
    'about_title':      'Over TWSStarter',
    'about_version':    'Versie',
    'about_copyright':  '© 2024 trade-commander.de',
    'about_desc':       'IBKR TWS / Gateway Launcher met automatische login',
    'help_title':       'TWSStarter — Help',
    'help_text':        '',
},

}


# ── Additional UI strings (v1.4: control row, modes, trace) ─────────────────
# Merged into STRINGS below. Product names "TWS"/"Gateway" stay untranslated.

_EXTRA: dict[str, dict[str, str]] = {
'en': {
    'lbl_default_mode': 'Default start',
    'mode_default':     'Default',
    'ctl_start':        'Start',
    'chk_all':          'All',
    'tip_all':          'Select / deselect all connections',
    'tip_start_tws':    'Start checked connections as TWS',
    'tip_start_gw':     'Start checked connections as Gateway',
    'tip_start_default':'Start checked connections in their default mode',
    'tip_stop':         'Stop checked connections',
    'trace_clear':      'Clear',
    'tip_trace_clear':  'Clear the trace log',
    'msg_none_checked': 'No connections checked.',
},
'de': {
    'lbl_default_mode': 'Standard-Start',
    'mode_default':     'Standard',
    'ctl_start':        'Start',
    'chk_all':          'Alle',
    'tip_all':          'Alle Verbindungen an-/abwählen',
    'tip_start_tws':    'Angehakte Verbindungen als TWS starten',
    'tip_start_gw':     'Angehakte Verbindungen als Gateway starten',
    'tip_start_default':'Angehakte Verbindungen im Standardmodus starten',
    'tip_stop':         'Angehakte Verbindungen stoppen',
    'trace_clear':      'Leeren',
    'tip_trace_clear':  'Trace-Anzeige leeren',
    'msg_none_checked': 'Keine Verbindung angehakt.',
},
'fr': {
    'lbl_default_mode': 'Démarrage par défaut',
    'mode_default':     'Défaut',
    'ctl_start':        'Démarrer',
    'chk_all':          'Tout',
    'tip_all':          'Tout sélectionner / désélectionner',
    'tip_start_tws':    'Démarrer les connexions cochées en TWS',
    'tip_start_gw':     'Démarrer les connexions cochées en Gateway',
    'tip_start_default':'Démarrer les connexions cochées dans leur mode par défaut',
    'tip_stop':         'Arrêter les connexions cochées',
    'trace_clear':      'Effacer',
    'tip_trace_clear':  'Effacer le journal',
    'msg_none_checked': 'Aucune connexion cochée.',
},
'es': {
    'lbl_default_mode': 'Inicio predeterminado',
    'mode_default':     'Predet.',
    'ctl_start':        'Iniciar',
    'chk_all':          'Todo',
    'tip_all':          'Seleccionar / deseleccionar todo',
    'tip_start_tws':    'Iniciar las conexiones marcadas como TWS',
    'tip_start_gw':     'Iniciar las conexiones marcadas como Gateway',
    'tip_start_default':'Iniciar las conexiones marcadas en su modo predeterminado',
    'tip_stop':         'Detener las conexiones marcadas',
    'trace_clear':      'Borrar',
    'tip_trace_clear':  'Borrar el registro',
    'msg_none_checked': 'Ninguna conexión marcada.',
},
'it': {
    'lbl_default_mode': 'Avvio predefinito',
    'mode_default':     'Predef.',
    'ctl_start':        'Avvia',
    'chk_all':          'Tutti',
    'tip_all':          'Seleziona / deseleziona tutto',
    'tip_start_tws':    'Avvia le connessioni selezionate come TWS',
    'tip_start_gw':     'Avvia le connessioni selezionate come Gateway',
    'tip_start_default':'Avvia le connessioni selezionate nella modalità predefinita',
    'tip_stop':         'Ferma le connessioni selezionate',
    'trace_clear':      'Pulisci',
    'tip_trace_clear':  'Pulisci il registro',
    'msg_none_checked': 'Nessuna connessione selezionata.',
},
'pl': {
    'lbl_default_mode': 'Domyślny start',
    'mode_default':     'Domyślny',
    'ctl_start':        'Uruchom',
    'chk_all':          'Wszystkie',
    'tip_all':          'Zaznacz / odznacz wszystkie',
    'tip_start_tws':    'Uruchom zaznaczone połączenia jako TWS',
    'tip_start_gw':     'Uruchom zaznaczone połączenia jako Gateway',
    'tip_start_default':'Uruchom zaznaczone połączenia w trybie domyślnym',
    'tip_stop':         'Zatrzymaj zaznaczone połączenia',
    'trace_clear':      'Wyczyść',
    'tip_trace_clear':  'Wyczyść dziennik',
    'msg_none_checked': 'Nie zaznaczono połączeń.',
},
'tr': {
    'lbl_default_mode': 'Varsayılan başlatma',
    'mode_default':     'Varsayılan',
    'ctl_start':        'Başlat',
    'chk_all':          'Tümü',
    'tip_all':          'Tümünü seç / kaldır',
    'tip_start_tws':    'Seçili bağlantıları TWS olarak başlat',
    'tip_start_gw':     'Seçili bağlantıları Gateway olarak başlat',
    'tip_start_default':'Seçili bağlantıları varsayılan modunda başlat',
    'tip_stop':         'Seçili bağlantıları durdur',
    'trace_clear':      'Temizle',
    'tip_trace_clear':  'İzleme günlüğünü temizle',
    'msg_none_checked': 'Hiçbir bağlantı seçilmedi.',
},
'pt': {
    'lbl_default_mode': 'Início padrão',
    'mode_default':     'Padrão',
    'ctl_start':        'Iniciar',
    'chk_all':          'Todos',
    'tip_all':          'Selecionar / desmarcar tudo',
    'tip_start_tws':    'Iniciar as conexões marcadas como TWS',
    'tip_start_gw':     'Iniciar as conexões marcadas como Gateway',
    'tip_start_default':'Iniciar as conexões marcadas no modo padrão',
    'tip_stop':         'Parar as conexões marcadas',
    'trace_clear':      'Limpar',
    'tip_trace_clear':  'Limpar o registro',
    'msg_none_checked': 'Nenhuma conexão marcada.',
},
'ja': {
    'lbl_default_mode': 'デフォルト起動',
    'mode_default':     'デフォルト',
    'ctl_start':        '開始',
    'chk_all':          'すべて',
    'tip_all':          'すべての接続を選択 / 解除',
    'tip_start_tws':    'チェックした接続を TWS で起動',
    'tip_start_gw':     'チェックした接続を Gateway で起動',
    'tip_start_default':'チェックした接続をデフォルトモードで起動',
    'tip_stop':         'チェックした接続を停止',
    'trace_clear':      'クリア',
    'tip_trace_clear':  'トレースをクリア',
    'msg_none_checked': '接続が選択されていません。',
},
'zh': {
    'lbl_default_mode': '默认启动',
    'mode_default':     '默认',
    'ctl_start':        '启动',
    'chk_all':          '全部',
    'tip_all':          '全选 / 取消全选',
    'tip_start_tws':    '将选中的连接以 TWS 启动',
    'tip_start_gw':     '将选中的连接以 Gateway 启动',
    'tip_start_default':'以默认模式启动选中的连接',
    'tip_stop':         '停止选中的连接',
    'trace_clear':      '清除',
    'tip_trace_clear':  '清除跟踪日志',
    'msg_none_checked': '未选中任何连接。',
},
'hi': {
    'lbl_default_mode': 'डिफ़ॉल्ट प्रारंभ',
    'mode_default':     'डिफ़ॉल्ट',
    'ctl_start':        'शुरू',
    'chk_all':          'सभी',
    'tip_all':          'सभी कनेक्शन चुनें / अचयनित करें',
    'tip_start_tws':    'चयनित कनेक्शन TWS के रूप में शुरू करें',
    'tip_start_gw':     'चयनित कनेक्शन Gateway के रूप में शुरू करें',
    'tip_start_default':'चयनित कनेक्शन उनके डिफ़ॉल्ट मोड में शुरू करें',
    'tip_stop':         'चयनित कनेक्शन रोकें',
    'trace_clear':      'साफ़ करें',
    'tip_trace_clear':  'ट्रेस लॉग साफ़ करें',
    'msg_none_checked': 'कोई कनेक्शन चयनित नहीं।',
},
'ru': {
    'lbl_default_mode': 'Запуск по умолчанию',
    'mode_default':     'По умолч.',
    'ctl_start':        'Запуск',
    'chk_all':          'Все',
    'tip_all':          'Выбрать / снять все соединения',
    'tip_start_tws':    'Запустить отмеченные соединения как TWS',
    'tip_start_gw':     'Запустить отмеченные соединения как Gateway',
    'tip_start_default':'Запустить отмеченные соединения в режиме по умолчанию',
    'tip_stop':         'Остановить отмеченные соединения',
    'trace_clear':      'Очистить',
    'tip_trace_clear':  'Очистить журнал',
    'msg_none_checked': 'Нет отмеченных соединений.',
},
'nl': {
    'lbl_default_mode': 'Standaardstart',
    'mode_default':     'Standaard',
    'ctl_start':        'Start',
    'chk_all':          'Alle',
    'tip_all':          'Alle verbindingen selecteren / deselecteren',
    'tip_start_tws':    'Aangevinkte verbindingen als TWS starten',
    'tip_start_gw':     'Aangevinkte verbindingen als Gateway starten',
    'tip_start_default':'Aangevinkte verbindingen in hun standaardmodus starten',
    'tip_stop':         'Aangevinkte verbindingen stoppen',
    'trace_clear':      'Wissen',
    'tip_trace_clear':  'Traceweergave wissen',
    'msg_none_checked': 'Geen verbindingen aangevinkt.',
},
}

for _lang, _extra in _EXTRA.items():
    STRINGS.setdefault(_lang, {}).update(_extra)


# ── Help text (v1.4) — overrides the initial _HELP above with the current docs ──

_HELP_CURRENT = {
'en': """
<h2>TWSStarter</h2>
<p>TWSStarter conveniently launches Interactive Brokers <b>Trader WorkStation
(TWS)</b> and <b>IB Gateway</b>, fills in the login automatically, monitors which
connections are running, and lets you start/stop several at once.</p>

<h3>Adding a Connection</h3>
<p>Click <b>＋ Add Connection</b>. Enter a name, your IBKR username, password,
choose <b>Live</b> or <b>Paper Trading</b>, and a <b>Default start</b> target
(<b>TWS</b> or <b>Gateway</b>) used by the "Start Default" button. Paths are
optional — leave blank to use the global defaults from Settings.</p>

<h3>Starting &amp; Stopping</h3>
<p>Tick the connections you want, then use the control row above the list:
<b>Start TWS</b>, <b>Start Gateway</b>, <b>Start Default</b> (per-connection
default) or <b>Stop</b> — each acts on the ticked connections. The <b>All</b>
checkbox selects/clears everything. Each running card also has its own red
<b>Stop</b> button. The login dialog is filled in automatically.</p>
<p><i>Keep the login window visible and do not move the mouse while autofill runs.</i></p>

<h3>Status</h3>
<p>
<span style="color:#334155">●</span> Grey = stopped &nbsp;
<span style="color:#f59e0b">●</span> Yellow = starting &nbsp;
<span style="color:#22c55e">●</span> Green = running.
The small icon next to the name shows whether <b>TWS</b> or <b>Gateway</b> is the
live connection.</p>

<h3>Runtime Monitoring</h3>
<p>TWSStarter detects running instances system-wide — also ones started in an
earlier session: <b>TWS</b> by its window title (account), <b>Gateway</b> by the
API port it listens on, mapped to the connection that launched it (learned once
on first start).</p>
<p><b>It only reports status — it never keeps TWS/Gateway running or restarts
them.</b> To keep TWS or Gateway up around the clock, use TWS's built-in
<b>Auto Restart</b>: instead of the daily logoff it restarts the app at a set
time, so the session and API stay alive. Enable it in TWS under
<i>Configuration → Lock and Exit → Auto Logoff Timer</i> — set the restart time
and select <b>Auto restart</b>.</p>

<h3>Trace &amp; Logs</h3>
<p>The black panel at the bottom traces every action with a timestamp:
white = info, <span style="color:#f59e0b">orange = warning</span>,
<span style="color:#ef4444">red = error</span>. <b>Clear</b> empties it. Full
logs are written to <code>%LocalAppData%\\TWSStarter\\log</code> (rotated, kept 3 days).</p>

<h3>Data &amp; Security</h3>
<p>All settings and connections are stored in
<code>%LocalAppData%\\TWSStarter\\config.json</code>. Passwords are encrypted with
AES-256 using a key bound to this machine, so the file cannot be decrypted on
another computer.</p>
""",

'de': """
<h2>TWSStarter</h2>
<p>TWSStarter startet die Interactive Brokers <b>Trader WorkStation (TWS)</b> und
den <b>IB Gateway</b> komfortabel, füllt den Login automatisch aus, überwacht
welche Verbindungen laufen und erlaubt das gleichzeitige Starten/Stoppen mehrerer
Verbindungen.</p>

<h3>Verbindung hinzufügen</h3>
<p>Klicken Sie auf <b>＋ Verbindung hinzufügen</b>. Geben Sie Bezeichnung,
IBKR-Benutzernamen, Passwort ein, wählen Sie <b>Live</b> oder <b>Paper Trading</b>
sowie den <b>Standard-Start</b> (<b>TWS</b> oder <b>Gateway</b>), den der Button
„Start Standard" verwendet. Pfade sind optional — leer = globale Einstellung.</p>

<h3>Starten &amp; Stoppen</h3>
<p>Haken Sie die gewünschten Verbindungen an und nutzen Sie die Steuerleiste über
der Liste: <b>Start TWS</b>, <b>Start Gateway</b>, <b>Start Standard</b>
(verbindungsspezifischer Standard) oder <b>Stop</b> — jeweils auf die angehakten
Verbindungen. Die <b>Alle</b>-Checkbox wählt alles an/ab. Jede laufende Karte hat
zusätzlich einen eigenen roten <b>Stop</b>-Button. Der Login wird automatisch
ausgefüllt.</p>
<p><i>Halten Sie das Login-Fenster sichtbar und bewegen Sie die Maus nicht während
des Ausfüllens.</i></p>

<h3>Statusanzeige</h3>
<p>
<span style="color:#334155">●</span> Grau = gestoppt &nbsp;
<span style="color:#f59e0b">●</span> Gelb = startet &nbsp;
<span style="color:#22c55e">●</span> Grün = läuft.
Das kleine Symbol neben dem Namen zeigt, ob <b>TWS</b> oder <b>Gateway</b> die
laufende Verbindung ist.</p>

<h3>Laufzeitüberwachung</h3>
<p>TWSStarter erkennt laufende Instanzen systemweit — auch in einer früheren
Sitzung gestartete: <b>TWS</b> über den Fenstertitel (Konto), <b>Gateway</b> über
den API-Port, auf dem es lauscht, zugeordnet zur startenden Verbindung (einmalig
beim ersten Start gelernt).</p>
<p><b>Die App meldet nur den Status — sie hält TWS/Gateway nicht am Laufen und
startet nichts neu.</b> Damit TWS oder Gateway rund um die Uhr laufen, nutzen Sie
die eingebaute <b>Auto Restart</b>-Funktion der TWS: statt der täglichen Abmeldung
wird die App zu einer festgelegten Zeit neu gestartet, sodass Sitzung und API
bestehen bleiben. Aktivieren in der TWS unter
<i>Configuration → Lock and Exit → Auto Logoff Timer</i> — Neustartzeit setzen und
<b>Auto restart</b> wählen.</p>

<h3>Trace &amp; Logs</h3>
<p>Der schwarze Bereich unten protokolliert jede Aktion mit Zeitstempel:
Weiß = Info, <span style="color:#f59e0b">Orange = Warnung</span>,
<span style="color:#ef4444">Rot = Fehler</span>. <b>Leeren</b> setzt ihn zurück.
Vollständige Logs liegen in <code>%LocalAppData%\\TWSStarter\\log</code>
(rotierend, 3 Tage aufbewahrt).</p>

<h3>Daten &amp; Sicherheit</h3>
<p>Alle Einstellungen und Verbindungen liegen in
<code>%LocalAppData%\\TWSStarter\\config.json</code>. Passwörter werden mit AES-256
verschlüsselt; der Schlüssel ist an diesen Rechner gebunden, sodass die Datei auf
einem anderen Computer nicht entschlüsselt werden kann.</p>
""",

'fr': """
<h2>TWSStarter</h2>
<p>TWSStarter lance commodément <b>Trader WorkStation (TWS)</b> et <b>IB Gateway</b>
d'Interactive Brokers, remplit la connexion automatiquement, surveille les
connexions actives et permet d'en démarrer/arrêter plusieurs à la fois.</p>

<h3>Ajouter une connexion</h3>
<p>Cliquez sur <b>＋ Ajouter une connexion</b>. Saisissez un nom, votre identifiant
IBKR, le mot de passe, choisissez <b>Live</b> ou <b>Paper Trading</b> et le
<b>démarrage par défaut</b> (<b>TWS</b> ou <b>Gateway</b>) utilisé par « Démarrer
par défaut ». Les chemins sont facultatifs.</p>

<h3>Démarrer &amp; Arrêter</h3>
<p>Cochez les connexions souhaitées, puis utilisez la barre au-dessus de la liste :
<b>Démarrer TWS</b>, <b>Démarrer Gateway</b>, <b>Démarrer par défaut</b> ou
<b>Stop</b> — sur les connexions cochées. La case <b>Tout</b> sélectionne/désélectionne.
Chaque carte active a aussi son propre bouton <b>Stop</b> rouge. La connexion est
remplie automatiquement.</p>
<p><i>Gardez la fenêtre visible et ne bougez pas la souris pendant le remplissage.</i></p>

<h3>Statut</h3>
<p>
<span style="color:#334155">●</span> Gris = arrêté &nbsp;
<span style="color:#f59e0b">●</span> Jaune = démarrage &nbsp;
<span style="color:#22c55e">●</span> Vert = en cours.
L'icône près du nom indique si <b>TWS</b> ou <b>Gateway</b> est la connexion active.</p>

<h3>Surveillance d'exécution</h3>
<p>TWSStarter détecte les instances actives à l'échelle du système — même lancées
lors d'une session précédente : <b>TWS</b> par le titre de la fenêtre (compte),
<b>Gateway</b> par le port API sur lequel il écoute, associé à la connexion qui l'a
lancé (appris au premier démarrage).</p>
<p><b>L'application ne fait que signaler l'état — elle ne maintient pas TWS/Gateway
en marche et ne redémarre rien.</b> Pour garder TWS ou Gateway actif en continu,
utilisez la fonction <b>Auto Restart</b> intégrée de TWS : au lieu de la
déconnexion quotidienne, l'application redémarre à une heure définie, la session
et l'API restant actives. Activez-la dans
<i>Configuration → Lock and Exit → Auto Logoff Timer</i> — réglez l'heure et
sélectionnez <b>Auto restart</b>.</p>

<h3>Trace &amp; Journaux</h3>
<p>Le panneau noir en bas trace chaque action avec horodatage : blanc = info,
<span style="color:#f59e0b">orange = avertissement</span>,
<span style="color:#ef4444">rouge = erreur</span>. <b>Effacer</b> le vide. Journaux
complets dans <code>%LocalAppData%\\TWSStarter\\log</code> (3 jours).</p>

<h3>Données &amp; Sécurité</h3>
<p>Tout est stocké dans <code>%LocalAppData%\\TWSStarter\\config.json</code>. Les mots
de passe sont chiffrés en AES-256 avec une clé liée à cette machine.</p>
""",

'es': """
<h2>TWSStarter</h2>
<p>TWSStarter inicia cómodamente <b>Trader WorkStation (TWS)</b> e <b>IB Gateway</b>
de Interactive Brokers, rellena el inicio de sesión automáticamente, supervisa qué
conexiones están activas y permite iniciar/detener varias a la vez.</p>

<h3>Agregar una conexión</h3>
<p>Haga clic en <b>＋ Agregar conexión</b>. Indique nombre, usuario IBKR,
contraseña, elija <b>Live</b> o <b>Paper Trading</b> y el <b>inicio predeterminado</b>
(<b>TWS</b> o <b>Gateway</b>) que usa «Iniciar predeterminado». Las rutas son
opcionales.</p>

<h3>Iniciar y detener</h3>
<p>Marque las conexiones y use la barra sobre la lista: <b>Iniciar TWS</b>,
<b>Iniciar Gateway</b>, <b>Iniciar predeterminado</b> o <b>Stop</b> — sobre las
marcadas. La casilla <b>Todo</b> selecciona/deselecciona. Cada tarjeta activa tiene
su propio botón <b>Stop</b> rojo. El inicio de sesión se rellena automáticamente.</p>
<p><i>Mantenga la ventana visible y no mueva el ratón durante el relleno.</i></p>

<h3>Estado</h3>
<p>
<span style="color:#334155">●</span> Gris = detenido &nbsp;
<span style="color:#f59e0b">●</span> Amarillo = iniciando &nbsp;
<span style="color:#22c55e">●</span> Verde = en ejecución.
El icono junto al nombre indica si <b>TWS</b> o <b>Gateway</b> es la conexión activa.</p>

<h3>Supervisión en ejecución</h3>
<p>TWSStarter detecta instancias activas en todo el sistema — también de sesiones
anteriores: <b>TWS</b> por el título de la ventana (cuenta), <b>Gateway</b> por el
puerto API en el que escucha, asociado a la conexión que lo inició (aprendido al
primer inicio).</p>
<p><b>La app solo informa del estado — no mantiene TWS/Gateway en marcha ni
reinicia nada.</b> Para mantener TWS o Gateway activo de forma continua, use la
función <b>Auto Restart</b> integrada de TWS: en lugar del cierre de sesión
diario, reinicia la aplicación a una hora fijada, manteniendo la sesión y la API.
Actívela en <i>Configuration → Lock and Exit → Auto Logoff Timer</i> — fije la hora
de reinicio y seleccione <b>Auto restart</b>.</p>

<h3>Traza y registros</h3>
<p>El panel negro inferior registra cada acción con marca de tiempo: blanco = info,
<span style="color:#f59e0b">naranja = aviso</span>,
<span style="color:#ef4444">rojo = error</span>. <b>Borrar</b> lo vacía. Registros
completos en <code>%LocalAppData%\\TWSStarter\\log</code> (3 días).</p>

<h3>Datos y seguridad</h3>
<p>Todo se guarda en <code>%LocalAppData%\\TWSStarter\\config.json</code>. Las
contraseñas se cifran con AES-256 con una clave ligada a este equipo.</p>
""",

'it': """
<h2>TWSStarter</h2>
<p>TWSStarter avvia comodamente <b>Trader WorkStation (TWS)</b> e <b>IB Gateway</b>
di Interactive Brokers, compila il login automaticamente, monitora quali
connessioni sono in esecuzione e permette di avviarne/fermarne più insieme.</p>

<h3>Aggiungere una connessione</h3>
<p>Fare clic su <b>＋ Aggiungi connessione</b>. Inserire nome, utente IBKR,
password, scegliere <b>Live</b> o <b>Paper Trading</b> e l'<b>avvio predefinito</b>
(<b>TWS</b> o <b>Gateway</b>) usato da «Avvia predefinito». I percorsi sono
facoltativi.</p>

<h3>Avviare e fermare</h3>
<p>Selezionare le connessioni e usare la barra sopra l'elenco: <b>Avvia TWS</b>,
<b>Avvia Gateway</b>, <b>Avvia predefinito</b> o <b>Stop</b> — sulle selezionate.
La casella <b>Tutti</b> seleziona/deseleziona. Ogni scheda attiva ha anche un
proprio pulsante <b>Stop</b> rosso. Il login viene compilato automaticamente.</p>
<p><i>Tenere la finestra visibile e non muovere il mouse durante la compilazione.</i></p>

<h3>Stato</h3>
<p>
<span style="color:#334155">●</span> Grigio = fermo &nbsp;
<span style="color:#f59e0b">●</span> Giallo = avvio &nbsp;
<span style="color:#22c55e">●</span> Verde = in esecuzione.
L'icona accanto al nome indica se <b>TWS</b> o <b>Gateway</b> è la connessione attiva.</p>

<h3>Monitoraggio runtime</h3>
<p>TWSStarter rileva le istanze attive a livello di sistema — anche avviate in una
sessione precedente: <b>TWS</b> dal titolo della finestra (conto), <b>Gateway</b>
dalla porta API su cui è in ascolto, associata alla connessione che l'ha avviato
(appresa al primo avvio).</p>
<p><b>L'app segnala solo lo stato — non mantiene TWS/Gateway in esecuzione né
riavvia nulla.</b> Per tenere TWS o Gateway sempre attivo, usare la funzione
<b>Auto Restart</b> integrata di TWS: invece della disconnessione giornaliera,
riavvia l'app a un orario impostato, mantenendo sessione e API. Attivarla in
<i>Configuration → Lock and Exit → Auto Logoff Timer</i> — impostare l'orario e
selezionare <b>Auto restart</b>.</p>

<h3>Trace e log</h3>
<p>Il pannello nero in basso registra ogni azione con orario: bianco = info,
<span style="color:#f59e0b">arancione = avviso</span>,
<span style="color:#ef4444">rosso = errore</span>. <b>Pulisci</b> lo svuota. Log
completi in <code>%LocalAppData%\\TWSStarter\\log</code> (3 giorni).</p>

<h3>Dati e sicurezza</h3>
<p>Tutto è salvato in <code>%LocalAppData%\\TWSStarter\\config.json</code>. Le password
sono crittografate con AES-256 con una chiave legata a questo computer.</p>
""",

'pl': """
<h2>TWSStarter</h2>
<p>TWSStarter wygodnie uruchamia <b>Trader WorkStation (TWS)</b> i <b>IB Gateway</b>
firmy Interactive Brokers, automatycznie wypełnia logowanie, monitoruje działające
połączenia i pozwala uruchamiać/zatrzymywać kilka naraz.</p>

<h3>Dodawanie połączenia</h3>
<p>Kliknij <b>＋ Dodaj połączenie</b>. Podaj nazwę, użytkownika IBKR, hasło, wybierz
<b>Live</b> lub <b>Paper Trading</b> oraz <b>domyślny start</b> (<b>TWS</b> lub
<b>Gateway</b>) używany przez „Uruchom domyślny". Ścieżki są opcjonalne.</p>

<h3>Uruchamianie i zatrzymywanie</h3>
<p>Zaznacz połączenia i użyj paska nad listą: <b>Uruchom TWS</b>, <b>Uruchom
Gateway</b>, <b>Uruchom domyślny</b> lub <b>Stop</b> — dla zaznaczonych. Pole
<b>Wszystkie</b> zaznacza/odznacza. Każda działająca karta ma własny czerwony
przycisk <b>Stop</b>. Logowanie jest wypełniane automatycznie.</p>
<p><i>Nie zasłaniaj okna logowania i nie ruszaj myszą podczas wypełniania.</i></p>

<h3>Status</h3>
<p>
<span style="color:#334155">●</span> Szary = zatrzymany &nbsp;
<span style="color:#f59e0b">●</span> Żółty = uruchamianie &nbsp;
<span style="color:#22c55e">●</span> Zielony = działa.
Ikona obok nazwy pokazuje, czy działa <b>TWS</b> czy <b>Gateway</b>.</p>

<h3>Monitorowanie</h3>
<p>TWSStarter wykrywa działające instancje w całym systemie — także z poprzedniej
sesji: <b>TWS</b> po tytule okna (konto), <b>Gateway</b> po porcie API, na którym
nasłuchuje, przypisane do połączenia, które je uruchomiło (uczone przy pierwszym
starcie).</p>
<p><b>Aplikacja tylko raportuje status — niczego nie restartuje.</b> Do
automatycznego restartu użyj funkcji TWS:
<i>TWS → Ustawienia → Lock and Exit → Auto Restart</i>.</p>

<h3>Trace i logi</h3>
<p>Czarny panel na dole zapisuje każdą akcję ze znacznikiem czasu: biały = info,
<span style="color:#f59e0b">pomarańczowy = ostrzeżenie</span>,
<span style="color:#ef4444">czerwony = błąd</span>. <b>Wyczyść</b> go opróżnia.
Pełne logi w <code>%LocalAppData%\\TWSStarter\\log</code> (3 dni).</p>

<h3>Dane i bezpieczeństwo</h3>
<p>Wszystko w <code>%LocalAppData%\\TWSStarter\\config.json</code>. Hasła są szyfrowane
AES-256 kluczem powiązanym z tym komputerem.</p>
""",

'tr': """
<h2>TWSStarter</h2>
<p>TWSStarter, Interactive Brokers <b>Trader WorkStation (TWS)</b> ve
<b>IB Gateway</b>'i rahatça başlatır, girişi otomatik doldurur, hangi bağlantıların
çalıştığını izler ve birden fazlasını aynı anda başlatıp durdurmanızı sağlar.</p>

<h3>Bağlantı Ekleme</h3>
<p><b>＋ Bağlantı Ekle</b>'ye tıklayın. Ad, IBKR kullanıcı adı, şifre girin,
<b>Live</b> veya <b>Paper Trading</b> ve „Varsayılan Başlat"ın kullandığı
<b>varsayılan başlatma</b>yı (<b>TWS</b> ya da <b>Gateway</b>) seçin. Yollar
isteğe bağlıdır.</p>

<h3>Başlatma ve Durdurma</h3>
<p>Bağlantıları işaretleyin ve listenin üstündeki çubuğu kullanın: <b>TWS Başlat</b>,
<b>Gateway Başlat</b>, <b>Varsayılan Başlat</b> veya <b>Stop</b> — işaretliler için.
<b>Tümü</b> kutusu hepsini seçer/kaldırır. Her çalışan kartın kendi kırmızı
<b>Stop</b> düğmesi de vardır. Giriş otomatik doldurulur.</p>
<p><i>Doldurma sırasında giriş penceresini görünür tutun ve fareyi oynatmayın.</i></p>

<h3>Durum</h3>
<p>
<span style="color:#334155">●</span> Gri = durduruldu &nbsp;
<span style="color:#f59e0b">●</span> Sarı = başlatılıyor &nbsp;
<span style="color:#22c55e">●</span> Yeşil = çalışıyor.
Adın yanındaki simge <b>TWS</b> mi <b>Gateway</b> mi çalıştığını gösterir.</p>

<h3>Çalışma Zamanı İzleme</h3>
<p>TWSStarter çalışan örnekleri sistem genelinde algılar — önceki oturumda
başlatılanlar dahil: <b>TWS</b> pencere başlığından (hesap), <b>Gateway</b>
dinlediği API portundan, onu başlatan bağlantıya eşlenerek (ilk başlatmada
öğrenilir).</p>
<p><b>Uygulama yalnızca durumu bildirir — hiçbir şeyi yeniden başlatmaz.</b> Otomatik
yeniden başlatma için TWS özelliğini kullanın:
<i>TWS → Ayarlar → Lock and Exit → Auto Restart</i>.</p>

<h3>İzleme ve Günlükler</h3>
<p>Alttaki siyah panel her eylemi zaman damgasıyla kaydeder: beyaz = bilgi,
<span style="color:#f59e0b">turuncu = uyarı</span>,
<span style="color:#ef4444">kırmızı = hata</span>. <b>Temizle</b> boşaltır. Tam
günlükler <code>%LocalAppData%\\TWSStarter\\log</code> içinde (3 gün).</p>

<h3>Veri ve Güvenlik</h3>
<p>Her şey <code>%LocalAppData%\\TWSStarter\\config.json</code> içinde saklanır.
Şifreler bu makineye bağlı bir anahtarla AES-256 ile şifrelenir.</p>
""",

'pt': """
<h2>TWSStarter</h2>
<p>O TWSStarter inicia comodamente o <b>Trader WorkStation (TWS)</b> e o
<b>IB Gateway</b> da Interactive Brokers, preenche o login automaticamente, monitora
quais conexões estão em execução e permite iniciar/parar várias de uma vez.</p>

<h3>Adicionar uma Conexão</h3>
<p>Clique em <b>＋ Adicionar conexão</b>. Informe nome, usuário IBKR, senha,
escolha <b>Live</b> ou <b>Paper Trading</b> e o <b>início padrão</b> (<b>TWS</b> ou
<b>Gateway</b>) usado por «Iniciar padrão». Os caminhos são opcionais.</p>

<h3>Iniciar e Parar</h3>
<p>Marque as conexões e use a barra acima da lista: <b>Iniciar TWS</b>,
<b>Iniciar Gateway</b>, <b>Iniciar padrão</b> ou <b>Stop</b> — nas marcadas. A caixa
<b>Todos</b> seleciona/desmarca. Cada cartão ativo tem seu próprio botão <b>Stop</b>
vermelho. O login é preenchido automaticamente.</p>
<p><i>Mantenha a janela visível e não mova o mouse durante o preenchimento.</i></p>

<h3>Status</h3>
<p>
<span style="color:#334155">●</span> Cinza = parado &nbsp;
<span style="color:#f59e0b">●</span> Amarelo = iniciando &nbsp;
<span style="color:#22c55e">●</span> Verde = em execução.
O ícone ao lado do nome mostra se <b>TWS</b> ou <b>Gateway</b> é a conexão ativa.</p>

<h3>Monitoramento</h3>
<p>O TWSStarter detecta instâncias ativas em todo o sistema — inclusive de uma
sessão anterior: <b>TWS</b> pelo título da janela (conta), <b>Gateway</b> pela porta
API em que escuta, associada à conexão que o iniciou (aprendida no primeiro início).</p>
<p><b>O app apenas informa o status — não mantém o TWS/Gateway em execução nem
reinicia nada.</b> Para manter o TWS ou Gateway ativo continuamente, use o recurso
<b>Auto Restart</b> integrado do TWS: em vez do logoff diário, ele reinicia o
aplicativo em um horário definido, mantendo a sessão e a API. Ative em
<i>Configuration → Lock and Exit → Auto Logoff Timer</i> — defina o horário e
selecione <b>Auto restart</b>.</p>

<h3>Trace e Logs</h3>
<p>O painel preto inferior registra cada ação com data/hora: branco = info,
<span style="color:#f59e0b">laranja = aviso</span>,
<span style="color:#ef4444">vermelho = erro</span>. <b>Limpar</b> esvazia. Logs
completos em <code>%LocalAppData%\\TWSStarter\\log</code> (3 dias).</p>

<h3>Dados e Segurança</h3>
<p>Tudo é salvo em <code>%LocalAppData%\\TWSStarter\\config.json</code>. As senhas são
criptografadas com AES-256 usando uma chave vinculada a este computador.</p>
""",

'ja': """
<h2>TWSStarter</h2>
<p>TWSStarter は Interactive Brokers の <b>Trader WorkStation (TWS)</b> と
<b>IB Gateway</b> を手軽に起動し、ログインを自動入力し、どの接続が稼働しているかを
監視し、複数をまとめて起動/停止できます。</p>

<h3>接続の追加</h3>
<p><b>＋ 接続を追加</b> をクリックし、名前・IBKRユーザー名・パスワードを入力、
<b>ライブ</b>か<b>ペーパー取引</b>、そして「デフォルト起動」が使う<b>デフォルト起動先</b>
(<b>TWS</b>か<b>Gateway</b>)を選びます。パスは任意です。</p>

<h3>起動と停止</h3>
<p>接続にチェックを入れ、リスト上部のバーを使います:<b>TWS 開始</b>、<b>Gateway 開始</b>、
<b>デフォルト 開始</b>、<b>Stop</b> — いずれもチェックした接続が対象です。<b>すべて</b>
チェックで全選択/解除。稼働中の各カードには赤い<b>Stop</b>ボタンもあります。ログインは
自動入力されます。</p>
<p><i>自動入力中はログイン画面を表示したまま、マウスを動かさないでください。</i></p>

<h3>ステータス</h3>
<p>
<span style="color:#334155">●</span> グレー = 停止 &nbsp;
<span style="color:#f59e0b">●</span> 黄 = 起動中 &nbsp;
<span style="color:#22c55e">●</span> 緑 = 稼働中。
名前の横のアイコンは <b>TWS</b> か <b>Gateway</b> のどちらが稼働中かを示します。</p>

<h3>稼働監視</h3>
<p>TWSStarter は稼働中のインスタンスをシステム全体で検出します（以前のセッションで
起動したものも):<b>TWS</b> はウィンドウタイトル(口座)で、<b>Gateway</b> は待ち受けて
いる API ポートで判定し、起動した接続に対応付けます(初回起動時に学習)。</p>
<p><b>本アプリは状態を表示するだけで、TWS/Gateway を稼働させ続けたり再起動したりはしません。</b>
TWS または Gateway を常時稼働させるには、TWS の <b>Auto Restart</b> 機能を使用してください:
毎日のログオフの代わりに指定した時刻でアプリを再起動し、セッションと API を維持します。
<i>Configuration → Lock and Exit → Auto Logoff Timer</i> で再起動時刻を設定し、
<b>Auto restart</b> を選択します。</p>

<h3>トレースとログ</h3>
<p>下部の黒い領域がすべての操作をタイムスタンプ付きで記録します:白 = 情報、
<span style="color:#f59e0b">オレンジ = 警告</span>、
<span style="color:#ef4444">赤 = エラー</span>。<b>クリア</b>で消去。完全なログは
<code>%LocalAppData%\\TWSStarter\\log</code>(3日間保持)。</p>

<h3>データとセキュリティ</h3>
<p>すべての設定と接続は <code>%LocalAppData%\\TWSStarter\\config.json</code> に保存され、
パスワードはこのPCに紐づく鍵で AES-256 暗号化されます。</p>
""",

'zh': """
<h2>TWSStarter</h2>
<p>TWSStarter 可便捷启动盈透证券的 <b>Trader WorkStation (TWS)</b> 和 <b>IB Gateway</b>，
自动填写登录，监控哪些连接正在运行，并可同时启动/停止多个连接。</p>

<h3>添加连接</h3>
<p>点击 <b>＋ 添加连接</b>。填写名称、IBKR 用户名、密码，选择<b>实盘</b>或<b>模拟交易</b>，
以及“启动默认”所用的<b>默认启动</b>（<b>TWS</b> 或 <b>Gateway</b>）。路径为可选。</p>

<h3>启动与停止</h3>
<p>勾选所需连接，使用列表上方的控制栏：<b>启动 TWS</b>、<b>启动 Gateway</b>、
<b>启动默认</b> 或 <b>Stop</b> —— 均作用于勾选的连接。<b>全部</b>复选框可全选/取消。
每个运行中的卡片还有自己的红色 <b>Stop</b> 按钮。登录将自动填写。</p>
<p><i>自动填写期间请保持登录窗口可见，不要移动鼠标。</i></p>

<h3>状态</h3>
<p>
<span style="color:#334155">●</span> 灰色 = 已停止 &nbsp;
<span style="color:#f59e0b">●</span> 黄色 = 启动中 &nbsp;
<span style="color:#22c55e">●</span> 绿色 = 运行中。
名称旁的图标显示当前运行的是 <b>TWS</b> 还是 <b>Gateway</b>。</p>

<h3>运行监控</h3>
<p>TWSStarter 在系统范围内检测运行中的实例——包括早前会话启动的：<b>TWS</b> 通过窗口
标题（账户），<b>Gateway</b> 通过其监听的 API 端口，并映射到启动它的连接（首次启动时学习）。</p>
<p><b>本应用仅报告状态——不会让 TWS/Gateway 保持运行，也不会重启任何程序。</b>
若要让 TWS 或 Gateway 全天候运行，请使用 TWS 内置的 <b>Auto Restart</b> 功能：
它不会每日注销，而是在设定时间重启应用，从而保持会话和 API 在线。
在 <i>Configuration → Lock and Exit → Auto Logoff Timer</i> 中设置重启时间并选择
<b>Auto restart</b>。</p>

<h3>跟踪与日志</h3>
<p>底部黑色面板记录每个操作并带时间戳：白色 = 信息，
<span style="color:#f59e0b">橙色 = 警告</span>，
<span style="color:#ef4444">红色 = 错误</span>。<b>清除</b>可清空。完整日志位于
<code>%LocalAppData%\\TWSStarter\\log</code>（保留 3 天）。</p>

<h3>数据与安全</h3>
<p>所有设置与连接保存在 <code>%LocalAppData%\\TWSStarter\\config.json</code>。密码以
绑定本机的密钥进行 AES-256 加密。</p>
""",

'hi': """
<h2>TWSStarter</h2>
<p>TWSStarter, Interactive Brokers के <b>Trader WorkStation (TWS)</b> और
<b>IB Gateway</b> को सुविधाजनक रूप से शुरू करता है, लॉगिन स्वतः भरता है, चालू
कनेक्शनों की निगरानी करता है और कई को एक साथ शुरू/रोकने देता है।</p>

<h3>कनेक्शन जोड़ें</h3>
<p><b>＋ कनेक्शन जोड़ें</b> पर क्लिक करें। नाम, IBKR उपयोगकर्ता नाम, पासवर्ड दर्ज करें,
<b>Live</b> या <b>Paper Trading</b> और „डिफ़ॉल्ट प्रारंभ" द्वारा उपयोग किया जाने वाला
<b>डिफ़ॉल्ट प्रारंभ</b> (<b>TWS</b> या <b>Gateway</b>) चुनें। पथ वैकल्पिक हैं।</p>

<h3>शुरू और बंद करें</h3>
<p>कनेक्शन चुनें और सूची के ऊपर की पट्टी का उपयोग करें: <b>TWS शुरू</b>,
<b>Gateway शुरू</b>, <b>डिफ़ॉल्ट शुरू</b> या <b>Stop</b> — चयनित पर। <b>सभी</b>
चेकबॉक्स सब चुनता/हटाता है। हर चालू कार्ड का अपना लाल <b>Stop</b> बटन भी है। लॉगिन
स्वतः भर जाता है।</p>
<p><i>ऑटोफिल के दौरान लॉगिन विंडो दृश्यमान रखें और माउस न हिलाएं।</i></p>

<h3>स्थिति</h3>
<p>
<span style="color:#334155">●</span> ग्रे = रुका &nbsp;
<span style="color:#f59e0b">●</span> पीला = शुरू हो रहा &nbsp;
<span style="color:#22c55e">●</span> हरा = चल रहा।
नाम के पास का आइकन दिखाता है कि <b>TWS</b> या <b>Gateway</b> चालू है।</p>

<h3>रनटाइम निगरानी</h3>
<p>TWSStarter चालू इंस्टेंस को पूरे सिस्टम में पहचानता है — पिछले सत्र में शुरू किए गए भी:
<b>TWS</b> विंडो शीर्षक (खाता) से, <b>Gateway</b> जिस API पोर्ट पर सुनता है उससे, उसे
शुरू करने वाले कनेक्शन से जोड़कर (पहले स्टार्ट पर सीखा गया)।</p>
<p><b>ऐप केवल स्थिति बताता है — कुछ भी पुनः आरंभ नहीं करता।</b> क्रैश के बाद स्वचालित
पुनः आरंभ के लिए TWS सुविधा का उपयोग करें:
<i>TWS → Settings → Lock and Exit → Auto Restart</i>।</p>

<h3>ट्रेस और लॉग</h3>
<p>नीचे का काला पैनल हर क्रिया को टाइमस्टैम्प के साथ दर्ज करता है: सफेद = जानकारी,
<span style="color:#f59e0b">नारंगी = चेतावनी</span>,
<span style="color:#ef4444">लाल = त्रुटि</span>। <b>साफ़ करें</b> इसे खाली करता है।
पूर्ण लॉग <code>%LocalAppData%\\TWSStarter\\log</code> में (3 दिन)।</p>

<h3>डेटा और सुरक्षा</h3>
<p>सब कुछ <code>%LocalAppData%\\TWSStarter\\config.json</code> में संग्रहीत है। पासवर्ड
इस मशीन से बंधी कुंजी के साथ AES-256 से एन्क्रिप्ट किए जाते हैं।</p>
""",

'ru': """
<h2>TWSStarter</h2>
<p>TWSStarter удобно запускает <b>Trader WorkStation (TWS)</b> и <b>IB Gateway</b>
Interactive Brokers, автоматически заполняет вход, отслеживает работающие соединения
и позволяет запускать/останавливать несколько сразу.</p>

<h3>Добавление соединения</h3>
<p>Нажмите <b>＋ Добавить соединение</b>. Укажите имя, логин IBKR, пароль, выберите
<b>Live</b> или <b>Paper Trading</b> и <b>запуск по умолчанию</b> (<b>TWS</b> или
<b>Gateway</b>), используемый кнопкой «Запуск по умолчанию». Пути необязательны.</p>

<h3>Запуск и остановка</h3>
<p>Отметьте соединения и используйте панель над списком: <b>Запуск TWS</b>,
<b>Запуск Gateway</b>, <b>Запуск по умолчанию</b> или <b>Stop</b> — для отмеченных.
Флажок <b>Все</b> выбирает/снимает всё. У каждой работающей карточки есть свой
красный кнопка <b>Stop</b>. Вход заполняется автоматически.</p>
<p><i>Не закрывайте окно входа и не двигайте мышь во время автозаполнения.</i></p>

<h3>Состояние</h3>
<p>
<span style="color:#334155">●</span> Серый = остановлен &nbsp;
<span style="color:#f59e0b">●</span> Жёлтый = запускается &nbsp;
<span style="color:#22c55e">●</span> Зелёный = работает.
Значок рядом с именем показывает, что запущено — <b>TWS</b> или <b>Gateway</b>.</p>

<h3>Мониторинг во время работы</h3>
<p>TWSStarter обнаруживает работающие экземпляры по всей системе — в том числе
запущенные в прошлой сессии: <b>TWS</b> по заголовку окна (счёт), <b>Gateway</b> по
API-порту, который он слушает, сопоставляя с соединением, запустившим его (выучено
при первом запуске).</p>
<p><b>Приложение только сообщает статус — оно не поддерживает работу TWS/Gateway и
ничего не перезапускает.</b> Чтобы TWS или Gateway работали круглосуточно,
используйте встроенную функцию <b>Auto Restart</b> в TWS: вместо ежедневного выхода
приложение перезапускается в заданное время, сохраняя сессию и API. Включите её в
<i>Configuration → Lock and Exit → Auto Logoff Timer</i> — задайте время перезапуска
и выберите <b>Auto restart</b>.</p>

<h3>Трассировка и логи</h3>
<p>Чёрная панель внизу фиксирует каждое действие с отметкой времени: белый = инфо,
<span style="color:#f59e0b">оранжевый = предупреждение</span>,
<span style="color:#ef4444">красный = ошибка</span>. <b>Очистить</b> очищает её.
Полные логи в <code>%LocalAppData%\\TWSStarter\\log</code> (3 дня).</p>

<h3>Данные и безопасность</h3>
<p>Всё хранится в <code>%LocalAppData%\\TWSStarter\\config.json</code>. Пароли шифруются
AES-256 ключом, привязанным к этому компьютеру.</p>
""",

'nl': """
<h2>TWSStarter</h2>
<p>TWSStarter start Interactive Brokers <b>Trader WorkStation (TWS)</b> en
<b>IB Gateway</b> op een handige manier, vult de login automatisch in, bewaakt
welke verbindingen actief zijn en laat u er meerdere tegelijk starten/stoppen.</p>

<h3>Verbinding toevoegen</h3>
<p>Klik op <b>＋ Verbinding toevoegen</b>. Voer een naam, uw IBKR-gebruikersnaam
en wachtwoord in, kies <b>Live</b> of <b>Paper Trading</b> en een
<b>standaardstart</b> (<b>TWS</b> of <b>Gateway</b>) die door de knop
"Start Standaard" wordt gebruikt. Paden zijn optioneel — laat leeg om de globale
standaarden uit Instellingen te gebruiken.</p>

<h3>Starten &amp; stoppen</h3>
<p>Vink de gewenste verbindingen aan en gebruik de knoppenrij boven de lijst:
<b>Start TWS</b>, <b>Start Gateway</b>, <b>Start Standaard</b> (standaard per
verbinding) of <b>Stoppen</b> — elk werkt op de aangevinkte verbindingen. Het
selectievakje <b>Alle</b> selecteert/wist alles. Elke actieve kaart heeft ook
een eigen rode knop <b>Stoppen</b>. Het inlogvenster wordt automatisch ingevuld.</p>
<p><i>Houd het inlogvenster zichtbaar en beweeg de muis niet terwijl het
automatisch invullen bezig is.</i></p>

<h3>Status</h3>
<p>
<span style="color:#334155">●</span> Grijs = gestopt &nbsp;
<span style="color:#f59e0b">●</span> Geel = bezig met starten &nbsp;
<span style="color:#22c55e">●</span> Groen = actief.
Het kleine pictogram naast de naam toont of <b>TWS</b> of <b>Gateway</b> de
actieve verbinding is.</p>

<h3>Runtime-bewaking</h3>
<p>TWSStarter detecteert actieve instanties systeembreed — ook die in een eerdere
sessie zijn gestart: <b>TWS</b> via de venstertitel (account), <b>Gateway</b> via
de API-poort waarop het luistert, gekoppeld aan de verbinding die het heeft
gestart (eenmalig geleerd bij de eerste start).</p>
<p><b>Het rapporteert alleen de status — het houdt TWS/Gateway niet draaiend en
herstart niets.</b> Om TWS of Gateway continu draaiend te houden, gebruikt u de
ingebouwde <b>Auto Restart</b>-functie van TWS: in plaats van de dagelijkse
afmelding wordt de app op een ingesteld tijdstip herstart, zodat de sessie en API
actief blijven. Schakel dit in via
<i>Configuration → Lock and Exit → Auto Logoff Timer</i> — stel de herstarttijd in
en selecteer <b>Auto restart</b>.</p>

<h3>Trace &amp; logs</h3>
<p>Het zwarte paneel onderaan registreert elke actie met een tijdstempel:
wit = info, <span style="color:#f59e0b">oranje = waarschuwing</span>,
<span style="color:#ef4444">rood = fout</span>. <b>Wissen</b> maakt het leeg.
Volledige logs worden geschreven naar <code>%LocalAppData%\\TWSStarter\\log</code>
(geroteerd, 3 dagen bewaard).</p>

<h3>Gegevens &amp; beveiliging</h3>
<p>Alle instellingen en verbindingen worden opgeslagen in
<code>%LocalAppData%\\TWSStarter\\config.json</code>. Wachtwoorden worden versleuteld
met AES-256 via een sleutel die aan deze computer is gebonden, zodat het bestand
niet op een andere computer kan worden ontsleuteld.</p>
""",
}

for _lang, _html in _HELP_CURRENT.items():
    STRINGS.setdefault(_lang, {})['help_text'] = _html


# ── Close-with-running-instances dialog buttons (v1.7) ──────────────────────
_CLOSE_STRINGS = {
    'en': {'dlg_active_close_all': 'Close all && exit',        'dlg_active_leave': 'Exit anyway'},
    'de': {'dlg_active_close_all': 'Alle schließen && beenden', 'dlg_active_leave': 'Trotzdem beenden'},
    'fr': {'dlg_active_close_all': 'Tout fermer et quitter',   'dlg_active_leave': 'Quitter quand même'},
    'es': {'dlg_active_close_all': 'Cerrar todo y salir',      'dlg_active_leave': 'Salir de todos modos'},
    'it': {'dlg_active_close_all': 'Chiudi tutto ed esci',     'dlg_active_leave': 'Esci comunque'},
    'ru': {'dlg_active_close_all': 'Закрыть всё и выйти',       'dlg_active_leave': 'Всё равно выйти'},
    'nl': {'dlg_active_close_all': 'Alles sluiten && afsluiten','dlg_active_leave': 'Toch afsluiten'},
    'pt': {'dlg_active_close_all': 'Fechar tudo e sair',       'dlg_active_leave': 'Sair mesmo assim'},
    'zh': {'dlg_active_close_all': '全部关闭并退出',              'dlg_active_leave': '仍然退出'},
    'ja': {'dlg_active_close_all': 'すべて閉じて終了',            'dlg_active_leave': 'そのまま終了'},
}
for _lang, _d in _CLOSE_STRINGS.items():
    STRINGS.setdefault(_lang, {}).update(_d)


# ── Per-connection autostart switch (v1.10) ─────────────────────────────────
_AUTOSTART_STRINGS = {
    'en': {'card_autostart': 'Autostart',      'tip_autostart': 'When on, start this connection automatically shortly after launch if it is not already running.', 'msg_autostart': "Autostart: starting '{name}' …"},
    'de': {'card_autostart': 'Autostart',      'tip_autostart': 'Wenn an, wird diese Verbindung kurz nach dem Start automatisch gestartet, falls sie nicht bereits läuft.', 'msg_autostart': "Autostart: '{name}' wird gestartet …"},
    'fr': {'card_autostart': 'Démarrage auto', 'tip_autostart': "Si activé, démarre cette connexion automatiquement peu après le lancement si elle n'est pas déjà en cours.", 'msg_autostart': "Démarrage auto : '{name}' …"},
    'es': {'card_autostart': 'Inicio auto',    'tip_autostart': 'Si está activado, inicia esta conexión automáticamente poco después del arranque si no está ya en ejecución.', 'msg_autostart': "Inicio auto: iniciando '{name}' …"},
    'it': {'card_autostart': 'Avvio auto',     'tip_autostart': "Se attivo, avvia questa connessione automaticamente poco dopo l'avvio se non è già in esecuzione.", 'msg_autostart': "Avvio auto: avvio di '{name}' …"},
    'ru': {'card_autostart': 'Автозапуск',     'tip_autostart': 'Если включено, запускает это соединение автоматически вскоре после старта, если оно ещё не работает.', 'msg_autostart': "Автозапуск: запуск '{name}' …"},
    'nl': {'card_autostart': 'Autostart',      'tip_autostart': 'Indien aan, start deze verbinding kort na het opstarten automatisch als ze nog niet draait.', 'msg_autostart': "Autostart: '{name}' wordt gestart …"},
    'pt': {'card_autostart': 'Início auto',    'tip_autostart': 'Se ativado, inicia esta conexão automaticamente logo após a inicialização se ainda não estiver em execução.', 'msg_autostart': "Início auto: iniciando '{name}' …"},
    'zh': {'card_autostart': '自动启动',        'tip_autostart': '开启后，若该连接尚未运行，将在启动后不久自动启动。', 'msg_autostart': "自动启动：正在启动 '{name}' …"},
    'ja': {'card_autostart': '自動起動',        'tip_autostart': 'オンの場合、起動直後にこの接続がまだ実行されていなければ自動的に起動します。', 'msg_autostart': "自動起動：'{name}' を起動しています …"},
}
for _lang, _d in _AUTOSTART_STRINGS.items():
    STRINGS.setdefault(_lang, {}).update(_d)


# ── Help restructuring (v1.8) ───────────────────────────────────────────────
# Applied to every supported language, driven by translated fragments below:
#   1. A prominent callout box under the title clarifying that TWSStarter only
#      launches/stops/shows status — it does NOT auto-start or keep TWS running;
#      for a 24/5 session use TWS's Auto Restart.
#   2. A "Settings" section (install paths for TWS/Gateway) with a screenshot.
#   3. Honest heading for the status section (it is not active monitoring).
#   4. Inline UI screenshots ([[IMG:...]] tokens, replaced by help_browser).

# 1. Callout box (inserted right after "<h2>TWSStarter</h2>").
_HELP_BOX = {
    'en': '<div class="callout"><b>TWSStarter starts TWS/Gateway and shows their status — it does not keep them running.</b> It starts and (when needed) stops your connections and can start them automatically at launch (the <b>Autostart</b> switch on each card). It does <b>not</b> restart them after a crash or the daily logoff. To keep TWS/Gateway running throughout the trading week, use TWS\'s built-in <b>Auto Restart</b>: <i>Configuration → Lock and Exit → Auto Logoff Timer</i> — set the time and select <b>Auto restart</b>.</div>',
    'de': '<div class="callout"><b>TWSStarter startet TWS/Gateway und zeigt deren Status — es hält sie nicht am Laufen.</b> Es startet und stoppt (bei Bedarf) Ihre Verbindungen und kann sie beim Programmstart automatisch starten (der <b>Autostart</b>-Schalter auf jeder Karte). Es startet sie <b>nicht</b> nach einem Absturz oder der täglichen Abmeldung neu. Damit TWS/Gateway die Handelswoche über durchlaufen, nutzen Sie die eingebaute <b>Auto Restart</b>-Funktion der TWS: <i>Configuration → Lock and Exit → Auto Logoff Timer</i> — Zeit setzen und <b>Auto restart</b> wählen.</div>',
    'fr': '<div class="callout"><b>TWSStarter démarre TWS/Gateway et affiche leur état — il ne les maintient pas en marche.</b> Il démarre et (au besoin) arrête vos connexions et peut les démarrer automatiquement au lancement (le commutateur <b>Autostart</b> sur chaque carte). Il ne les redémarre <b>pas</b> après un plantage ou la déconnexion quotidienne. Pour garder TWS/Gateway actif toute la semaine de bourse, utilisez la fonction <b>Auto Restart</b> intégrée de TWS : <i>Configuration → Lock and Exit → Auto Logoff Timer</i> — réglez l\'heure et sélectionnez <b>Auto restart</b>.</div>',
    'es': '<div class="callout"><b>TWSStarter inicia TWS/Gateway y muestra su estado — no los mantiene en ejecución.</b> Inicia y (si hace falta) detiene sus conexiones y puede iniciarlas automáticamente al arrancar (el interruptor <b>Autostart</b> en cada tarjeta). <b>No</b> las reinicia tras un fallo o el cierre de sesión diario. Para mantener TWS/Gateway en ejecución durante la semana bursátil, use la función <b>Auto Restart</b> integrada de TWS: <i>Configuration → Lock and Exit → Auto Logoff Timer</i> — fije la hora y seleccione <b>Auto restart</b>.</div>',
    'it': '<div class="callout"><b>TWSStarter avvia TWS/Gateway e ne mostra lo stato — non li mantiene in esecuzione.</b> Avvia e (se serve) ferma le tue connessioni e può avviarle automaticamente all\'avvio (l\'interruttore <b>Autostart</b> su ogni scheda). <b>Non</b> le riavvia dopo un crash o la disconnessione giornaliera. Per tenere TWS/Gateway attivo per tutta la settimana di borsa, usare la funzione <b>Auto Restart</b> integrata di TWS: <i>Configuration → Lock and Exit → Auto Logoff Timer</i> — impostare l\'orario e selezionare <b>Auto restart</b>.</div>',
    'ru': '<div class="callout"><b>TWSStarter запускает TWS/Gateway и показывает их статус — он не поддерживает их работу.</b> Он запускает и при необходимости останавливает ваши соединения и может запускать их автоматически при старте (переключатель <b>Autostart</b> на каждой карточке). Он <b>не</b> перезапускает их после сбоя или ежедневного выхода. Чтобы TWS/Gateway работали в течение торговой недели, используйте встроенную функцию <b>Auto Restart</b> в TWS: <i>Configuration → Lock and Exit → Auto Logoff Timer</i> — задайте время и выберите <b>Auto restart</b>.</div>',
    'nl': '<div class="callout"><b>TWSStarter start TWS/Gateway en toont hun status — het houdt ze niet draaiend.</b> Het start en stopt (indien nodig) uw verbindingen en kan ze automatisch starten bij het opstarten (de <b>Autostart</b>-schakelaar op elke kaart). Het herstart ze <b>niet</b> na een crash of de dagelijkse afmelding. Om TWS/Gateway de hele handelsweek draaiend te houden, gebruikt u de ingebouwde <b>Auto Restart</b>-functie van TWS: <i>Configuration → Lock and Exit → Auto Logoff Timer</i> — stel de tijd in en selecteer <b>Auto restart</b>.</div>',
    'pt': '<div class="callout"><b>O TWSStarter inicia o TWS/Gateway e mostra o status — não os mantém em execução.</b> Ele inicia e (se preciso) para suas conexões e pode iniciá-las automaticamente ao abrir (o botão <b>Autostart</b> em cada cartão). <b>Não</b> as reinicia após uma falha ou o logoff diário. Para manter o TWS/Gateway em execução durante a semana de negociação, use o recurso <b>Auto Restart</b> integrado do TWS: <i>Configuration → Lock and Exit → Auto Logoff Timer</i> — defina o horário e selecione <b>Auto restart</b>.</div>',
    'zh': '<div class="callout"><b>TWSStarter 启动 TWS/Gateway 并显示其状态——但不会让它们保持运行。</b> 它启动并（必要时）停止你的连接，还能在程序启动时自动启动它们（每张卡片上的 <b>Autostart</b> 开关）。它<b>不会</b>在崩溃或每日注销后重启它们。若要让 TWS/Gateway 在整个交易周内持续运行，请使用 TWS 内置的 <b>Auto Restart</b> 功能：<i>Configuration → Lock and Exit → Auto Logoff Timer</i> —— 设置时间并选择 <b>Auto restart</b>。</div>',
    'ja': '<div class="callout"><b>TWSStarter は TWS/Gateway を起動して状態を表示します — 稼働させ続けはしません。</b> 接続を起動し、必要に応じて停止し、起動時に自動的に開始することもできます（各カードの <b>Autostart</b> スイッチ）。クラッシュや毎日のログオフの後に再起動は<b>しません</b>。取引週の間 TWS/Gateway を動かし続けるには、TWS 内蔵の <b>Auto Restart</b> 機能を使用してください：<i>Configuration → Lock and Exit → Auto Logoff Timer</i> —— 時刻を設定して <b>Auto restart</b> を選択します。</div>',
}

# 1b. Autostart paragraph, appended to the "Starting & Stopping" section.
_HELP_AUTOSTART = {
    'en': '<p>Each card has an <b>Autostart</b> switch (on by default). A few seconds after TWSStarter starts, every connection whose switch is on and that is not already running is started automatically in its default mode. This runs once at launch — it is not a watchdog and does not restart anything later.</p>',
    'de': '<p>Jede Karte hat einen <b>Autostart</b>-Schalter (standardmäßig an). Wenige Sekunden nach dem Start von TWSStarter wird jede Verbindung mit aktiviertem Schalter, die nicht bereits läuft, automatisch im Standardmodus gestartet. Das geschieht einmalig beim Start — es ist kein Watchdog und startet später nichts neu.</p>',
    'fr': '<p>Chaque carte possède un commutateur <b>Autostart</b> (activé par défaut). Quelques secondes après le lancement de TWSStarter, chaque connexion dont le commutateur est activé et qui n\'est pas déjà en cours est démarrée automatiquement dans son mode par défaut. Cela s\'exécute une seule fois au lancement — ce n\'est pas un chien de garde et ne redémarre rien par la suite.</p>',
    'es': '<p>Cada tarjeta tiene un interruptor <b>Autostart</b> (activado por defecto). Unos segundos después de iniciar TWSStarter, cada conexión con el interruptor activado que no esté ya en ejecución se inicia automáticamente en su modo predeterminado. Ocurre una sola vez al arrancar — no es un vigilante y no reinicia nada después.</p>',
    'it': '<p>Ogni scheda ha un interruttore <b>Autostart</b> (attivo per impostazione predefinita). Pochi secondi dopo l\'avvio di TWSStarter, ogni connessione con l\'interruttore attivo e non già in esecuzione viene avviata automaticamente nella sua modalità predefinita. Avviene una sola volta all\'avvio — non è un watchdog e non riavvia nulla in seguito.</p>',
    'ru': '<p>На каждой карточке есть переключатель <b>Autostart</b> (по умолчанию включён). Через несколько секунд после запуска TWSStarter каждое соединение с включённым переключателем, которое ещё не работает, автоматически запускается в своём режиме по умолчанию. Это выполняется один раз при запуске — это не watchdog и ничего не перезапускает позже.</p>',
    'nl': '<p>Elke kaart heeft een <b>Autostart</b>-schakelaar (standaard aan). Enkele seconden na het starten van TWSStarter wordt elke verbinding waarvan de schakelaar aan staat en die nog niet draait automatisch gestart in haar standaardmodus. Dit gebeurt eenmalig bij het opstarten — het is geen watchdog en herstart later niets.</p>',
    'pt': '<p>Cada cartão tem um botão <b>Autostart</b> (ativado por padrão). Alguns segundos após iniciar o TWSStarter, cada conexão com o botão ativado e que ainda não esteja em execução é iniciada automaticamente no seu modo padrão. Isto ocorre uma vez na inicialização — não é um watchdog e não reinicia nada depois.</p>',
    'zh': '<p>每张卡片都有一个 <b>Autostart</b> 开关（默认开启）。TWSStarter 启动几秒后，凡是开关开启且尚未运行的连接都会以其默认模式自动启动。这只在启动时执行一次——它不是看门狗，之后不会重启任何程序。</p>',
    'ja': '<p>各カードには <b>Autostart</b> スイッチがあります（既定でオン）。TWSStarter の起動から数秒後、スイッチがオンでまだ実行されていない各接続が、既定のモードで自動的に起動します。これは起動時に一度だけ実行され、ウォッチドッグではなく、その後の再起動は行いません。</p>',
}

# 2. Settings section (inserted before "Adding a Connection"). Ends with the
#    settings screenshot.
_HELP_SETTINGS = {
    'en': '<h3>Settings — where TWS/Gateway are installed</h3>\n<p>This is fundamental. Open <b>Settings</b> (top right) and set the install directories for <b>TWS</b> and <b>IB Gateway</b>. They are used as the defaults whenever a connection does not specify its own paths, so you usually set them once here.</p>\n[[IMG:settings]]\n',
    'de': '<h3>Einstellungen — wo TWS/Gateway installiert sind</h3>\n<p>Das ist grundlegend. Öffnen Sie die <b>Einstellungen</b> (oben rechts) und tragen Sie die Installationsverzeichnisse von <b>TWS</b> und <b>IB Gateway</b> ein. Sie werden als Standard verwendet, wann immer eine Verbindung keine eigenen Pfade angibt — Sie legen sie also normalerweise einmal hier fest.</p>\n[[IMG:settings]]\n',
    'fr': '<h3>Paramètres — où TWS/Gateway sont installés</h3>\n<p>C\'est fondamental. Ouvrez les <b>Paramètres</b> (en haut à droite) et indiquez les répertoires d\'installation de <b>TWS</b> et d\'<b>IB Gateway</b>. Ils servent de valeurs par défaut lorsqu\'une connexion n\'indique pas ses propres chemins ; vous les définissez donc généralement une seule fois ici.</p>\n[[IMG:settings]]\n',
    'es': '<h3>Configuración — dónde están instalados TWS/Gateway</h3>\n<p>Es fundamental. Abra <b>Configuración</b> (arriba a la derecha) e indique los directorios de instalación de <b>TWS</b> e <b>IB Gateway</b>. Se usan como predeterminados cuando una conexión no especifica sus propias rutas, así que normalmente se definen una vez aquí.</p>\n[[IMG:settings]]\n',
    'it': '<h3>Impostazioni — dove sono installati TWS/Gateway</h3>\n<p>È fondamentale. Aprire <b>Impostazioni</b> (in alto a destra) e indicare le cartelle di installazione di <b>TWS</b> e <b>IB Gateway</b>. Vengono usate come predefinite quando una connessione non specifica percorsi propri, quindi di solito si impostano una volta qui.</p>\n[[IMG:settings]]\n',
    'ru': '<h3>Настройки — где установлены TWS/Gateway</h3>\n<p>Это основное. Откройте <b>Настройки</b> (вверху справа) и укажите каталоги установки <b>TWS</b> и <b>IB Gateway</b>. Они используются по умолчанию, когда у соединения не заданы собственные пути, поэтому обычно их задают один раз здесь.</p>\n[[IMG:settings]]\n',
    'nl': '<h3>Instellingen — waar TWS/Gateway zijn geïnstalleerd</h3>\n<p>Dit is essentieel. Open <b>Instellingen</b> (rechtsboven) en stel de installatiemappen van <b>TWS</b> en <b>IB Gateway</b> in. Ze worden als standaard gebruikt wanneer een verbinding geen eigen paden opgeeft, dus meestal stelt u ze hier één keer in.</p>\n[[IMG:settings]]\n',
    'pt': '<h3>Configurações — onde o TWS/Gateway estão instalados</h3>\n<p>Isto é fundamental. Abra <b>Configurações</b> (canto superior direito) e informe as pastas de instalação do <b>TWS</b> e do <b>IB Gateway</b>. Elas são usadas como padrão quando uma conexão não especifica os próprios caminhos, então normalmente você as define uma vez aqui.</p>\n[[IMG:settings]]\n',
    'zh': '<h3>设置 —— TWS/Gateway 的安装位置</h3>\n<p>这是基础。打开<b>设置</b>（右上角），填写 <b>TWS</b> 和 <b>IB Gateway</b> 的安装目录。当某个连接未指定自己的路径时，它们将作为默认值，因此通常在此处设置一次即可。</p>\n[[IMG:settings]]\n',
    'ja': '<h3>設定 —— TWS/Gateway のインストール場所</h3>\n<p>これは基本です。<b>設定</b>（右上）を開き、<b>TWS</b> と <b>IB Gateway</b> のインストールフォルダを指定します。接続が独自のパスを指定していない場合の既定値として使われるため、通常はここで一度設定します。</p>\n[[IMG:settings]]\n',
}

# 3. Rename the "monitoring" heading (old -> new) — it only reports status.
_HELP_STATUS_HEADING = {
    'en': ('<h3>Runtime Monitoring</h3>', '<h3>Which instances are running</h3>'),
    'de': ('<h3>Laufzeitüberwachung</h3>', '<h3>Welche Instanzen laufen</h3>'),
    'fr': ("<h3>Surveillance d'exécution</h3>", '<h3>Quelles instances sont en cours</h3>'),
    'es': ('<h3>Supervisión en ejecución</h3>', '<h3>Qué instancias están en ejecución</h3>'),
    'it': ('<h3>Monitoraggio runtime</h3>', '<h3>Quali istanze sono in esecuzione</h3>'),
    'ru': ('<h3>Мониторинг во время работы</h3>', '<h3>Какие экземпляры запущены</h3>'),
    'nl': ('<h3>Runtime-bewaking</h3>', '<h3>Welke instanties draaien</h3>'),
    'pt': ('<h3>Monitoramento</h3>', '<h3>Quais instâncias estão em execução</h3>'),
    'zh': ('<h3>运行监控</h3>', '<h3>哪些实例正在运行</h3>'),
    'ja': ('<h3>稼働監視</h3>', '<h3>稼働中のインスタンス</h3>'),
}

for _code in LANGUAGES:
    _help = STRINGS.get(_code, {}).get("help_text", "")
    _old, _new = _HELP_STATUS_HEADING[_code]
    _help = _help.replace(_old, _new, 1)
    _help = _help.replace(
        "<h2>TWSStarter</h2>", "<h2>TWSStarter</h2>\n" + _HELP_BOX[_code], 1
    )
    # Split on <h3>: [0] is the intro (title + box), the rest are sections.
    _sections = _help.split("<h3>")
    _sections[0] = _sections[0].rstrip() + "\n[[IMG:main]]\n"
    _rest = ["<h3>" + _s for _s in _sections[1:]]
    if _rest:  # add-connection screenshot inside the first real section
        _rest[0] = _rest[0].rstrip() + "\n[[IMG:add]]\n"
    if len(_rest) > 1:  # Autostart note at the end of "Starting & Stopping"
        _rest[1] = _rest[1].rstrip() + "\n" + _HELP_AUTOSTART[_code] + "\n"
    # Settings section goes between the intro and "Adding a Connection".
    STRINGS[_code]["help_text"] = _sections[0] + _HELP_SETTINGS[_code] + "".join(_rest)
