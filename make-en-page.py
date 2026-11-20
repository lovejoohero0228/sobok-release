# docs/index.html (한국어) 에서 docs/en/index.html (영어) 을 만든다. 모양과 스크립트는 그대로 두고 글만 바꾼다.
import io, os, re
src = 'docs/index.html'
s = io.open(src, encoding='utf-8').read()
left = []
def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b)

PROMPT_EN = '''Please install Sobok on my computer. It's a desktop widget that makes it snow on my screen.

■ If you can run commands on this computer yourself
1. Check the operating system yourself. Don't ask me.
2. Run the matching command exactly as written.
   Windows: powershell -c "irm https://raw.githubusercontent.com/lovejoohero0228/sobok-release/main/install.ps1 | iex"
   Mac: curl -fsSL https://raw.githubusercontent.com/lovejoohero0228/sobok-release/main/install-mac.sh | bash
3. Check that the sobok process is running, then tell me "All done! Look at your screen, it should be snowing."
   On a Mac, also add "If a window asks for Accessibility access, please turn Sobok on."
- Don't change a single character of the command. Don't use admin rights (sudo) and don't install anything else.
- Don't ask me to type commands. If there's an error, find out why and try once more.

■ If you can't run commands yourself (a web or phone chat)
Don't pretend you installed it. Follow these steps only.
1. Show the text below exactly and wait for my answer. Always show the choices, one per line. If you can show tappable choice buttons, use them.
   I can't install things on your computer from here. Do you already use an AI that works directly on your computer, like the Codex app, Claude Code, Cowork in the Claude desktop app, or Cursor?
   1) Yes, I do
   2) No, or I'm not sure
   (You can just send the number)
2. If I say yes, show the text below exactly and stop.
   Great! Then please do this.
   1) Open that app and start a new chat.
   2) Copy the first message you just sent me, from start to end, and paste it there. It's the one that starts with "Please install Sobok on my computer".
   3) If it asks whether it can run a command, allow it. That AI will do the install for you.
3. If I say no or I'm not sure, don't recommend a new app. Walk me through installing it by hand. First ask "1) Windows  2) Mac", then give one step at a time. Move on when I say "done".
   Windows
   1) Press the Windows key and R together. A small "Run" box appears.
   2) Copy the Windows command above, paste it into that box, and press Enter.
   3) A blue window flashes and closes. When it starts snowing, you're done.
   Mac
   1) Open Finder and double-click Applications → Utilities → Terminal. (If you use the search bar instead, click the black "Terminal" app itself rather than pressing Enter.)
   2) Copy the Mac command above, paste it into the window that opened, and press Enter.
   3) When it starts snowing, you're done. If a window asks for "Accessibility" access, please turn Sobok on.
   When you show a command, put it on one line in a code block so it's easy to copy.'''

# 프롬프트 본문 통째로
i = s.index('<span id="c5">') + len('<span id="c5">'); j = s.index('</span><button data-copy="c5">')
s = s[:i] + PROMPT_EN + s[j:]

D = 'Snow piles up softly on your screen. Pack it, roll it, and build little snowmen that talk. A cozy winter desktop widget.'
PAIRS = [
 ('<html lang="ko">', '<html lang="en">'),
 ('<title>소복소복 — 화면 속으로 겨울이 찾아왔어요</title>', '<title>Sobok — winter comes to your screen</title>'),
 ('<meta name="description" content="내 화면에 눈이 소복소복 쌓여요. 눈을 뭉쳐 굴리고, 말 거는 눈사람도 만들 수 있는 겨울 데스크탑 위젯.">', '<meta name="description" content="%s">' % D),
 ('<meta property="og:site_name" content="소복소복">', '<meta property="og:site_name" content="Sobok">'),
 ('<meta property="og:title" content="소복소복 — 화면 속으로 겨울이 찾아왔어요">', '<meta property="og:title" content="Sobok — winter comes to your screen">'),
 ('<meta property="og:description" content="내 화면에 눈이 소복소복 쌓여요. 눈을 뭉쳐 굴리고, 말 거는 눈사람도 만들 수 있는 겨울 데스크탑 위젯.">', '<meta property="og:description" content="%s">' % D),
 ('<meta property="og:url" content="https://lovejoohero0228.github.io/sobok-release/">', '<meta property="og:url" content="https://lovejoohero0228.github.io/sobok-release/en/">'),
 ('<meta property="og:locale" content="ko_KR">', '<meta property="og:locale" content="en_US">'),
 # 머리
 ('<p class="kicker">화면 속으로 겨울이 찾아왔어요</p>', '<p class="kicker">Winter comes to your screen</p>'),
 ('<h1>소복소복</h1>', '<h1>Sobok</h1>'),
 ('<p>내 화면에 눈이 소복소복 쌓여요.</p>', '<p>Snow piles up softly on your screen.<br><small style="opacity:.8">소복소복 <i>(sobok-sobok)</i>: the Korean word for snow quietly piling up.</small></p>'),
 ('<li>Windows 10 · 11 또는 Mac</li>', '<li>Windows 10 · 11 or Mac</li>'),
 ('<li>설치는 1분이면 돼요</li>', '<li>Installs in about a minute</li>'),
 ('<a href="#install">시작하기</a><a href="#play">눈사람 만드는 법</a><a href="#tips">이런 것도 돼요</a><a href="#settings">설정 바꾸기</a><a href="#remove">소복소복 지우기</a>',
  '<a href="#install">Get started</a><a href="#play">Build a snowman</a><a href="#tips">More to try</a><a href="#settings">Settings</a><a href="#remove">Uninstall</a>'),
 ('<div class="pcnote"><b>💻 PC 전용 프로그램이에요.</b> Windows 와 Mac 컴퓨터에서 쓸 수 있어요.', '<div class="pcnote"><b>💻 Sobok is for computers.</b> It runs on Windows and Mac.'),
 ('📱 <b>폰으로 보고 계신다면:</b> 설치는 PC 에서만 할 수 있어요. 이 페이지 주소를 PC 로 보내서 PC 브라우저로 열어 주세요. 그러면 설치 방법을 바로 복사해 넣을 수 있어요.',
  '📱 <b>On your phone?</b> You can only install it on a computer. Send this page to your computer and open it there, so you can copy the install command right away.'),
 ('<p class="lead">눈을 뭉쳐 굴리고, 눈사람도 만들 수 있어요.<br>근데 얘네… 둘이 붙여 놓으면 수다도 떠네요?</p>', '<p class="lead">Pack the snow, roll it, and build a snowman.<br>And these guys… put two together and they start chatting?</p>'),
 # 시작하기
 ('<h2 data-n="01">시작하기</h2>', '<h2 data-n="01">Get started</h2>'),
 ('</svg>AI로 설치</button>', '</svg>Install with AI</button>'),
 ('<h3><i>1</i>AI에게 시키기</h3>', '<h3><i>1</i>Ask your AI</h3>'),
 ('<li><b>내 컴퓨터에서 직접 일하는 AI</b>를 열어요. <small>Codex 앱, Claude Code, Claude 데스크톱 앱의 Cowork, Cursor 같은 것들이에요.</small></li>',
  '<li>Open <b>an AI that works directly on your computer</b>. <small>For example the Codex app, Claude Code, Cowork in the Claude desktop app, or Cursor.</small></li>'),
 ('<li>아래 <b>복사하기</b>를 눌러 AI에게 붙여 넣고 보내요.</li>', '<li>Press <b>Copy</b> below, paste it to your AI, and send.</li>'),
 ('<li>AI가 명령을 실행해도 되는지 물으면 허용해 주세요. 설치가 끝나면 소복소복이 저절로 켜져요.</li>', '<li>If the AI asks whether it can run a command, allow it. Sobok starts by itself when the install finishes.</li>'),
 ('<p class="ok">✅ 화면에 눈이 내리기 시작하면 성공이에요.</p>', '<p class="ok">✅ When it starts snowing on your screen, it worked.</p>'),
 ('<p class="note">이런 AI를 써 본 적이 없다면 위의 Windows / Mac 탭이 더 빨라요. 평소 쓰는 ChatGPT 나 Claude 대화창에 붙여 넣어도 같은 방법을 한 단계씩 알려 줘요.</p>',
  '<p class="note">Never used an AI like that? The Windows / Mac tabs above are faster. You can also paste this into a regular ChatGPT or Claude chat and it will walk you through the same steps one at a time.</p>'),
 ('<p>다음부터는 시작 메뉴(Windows)나 화면 위쪽 돋보기(Mac)에서 <b>소복소복</b>을 검색해서 클릭해요.</p>', '<p>Next time, search for <b>Sobok</b> in the Start menu (Windows) or Spotlight (Mac) and click it.</p>'),
 ('<h3><i>1</i>설치하기</h3>', '<h3><i>1</i>Install</h3>'),
 ('<h3 id="run"><i>2</i>실행하기</h3>', '<h3 id="run"><i>2</i>Open it</h3>'),
 ('<h3><i>2</i>실행하기</h3>', '<h3><i>2</i>Open it</h3>'),
 ('<li>아래 <b>복사하기</b>를 눌러요.</li>', '<li>Press <b>Copy</b> below.</li>'),
 ('<li><kbd>Windows 키</kbd> + <kbd>R</kbd> 을 같이 눌러요.</li>', '<li>Press the <kbd>Windows key</kbd> + <kbd>R</kbd> together.</li>'),
 ('<li>뜬 <b>실행</b> 창에 <kbd>Ctrl</kbd> + <kbd>V</kbd> 로 붙여 넣고 <kbd>Enter</kbd> 를 눌러요.</li>', '<li>In the <b>Run</b> box that appears, paste with <kbd>Ctrl</kbd> + <kbd>V</kbd> and press <kbd>Enter</kbd>.</li>'),
 ('<li>설치가 끝나면 소복소복이 저절로 켜져요.</li>', '<li>Sobok starts by itself when the install finishes.</li>'),
 ('<p>시작 메뉴에서 <b>소복소복</b>을 검색해서 클릭해요.</p>', '<p>Search for <b>Sobok</b> in the Start menu and click it.</p>'),
 ('<li><b>Finder</b> 에서 <b>응용 프로그램 → 유틸리티 → 터미널</b>을 더블클릭해서 열어요. 검색창(<kbd>⌘</kbd> + <kbd>Space</kbd>)으로 찾을 때는 Enter 대신 검은 창 모양의 <b>터미널</b> 앱을 직접 클릭해요.</li>',
  '<li>In <b>Finder</b>, double-click <b>Applications → Utilities → Terminal</b>. If you use Spotlight (<kbd>⌘</kbd> + <kbd>Space</kbd>) instead, click the black <b>Terminal</b> app itself rather than pressing Enter.</li>'),
 ('<li><kbd>⌘</kbd> + <kbd>V</kbd> 로 붙여 넣고 <kbd>Enter</kbd> 를 눌러요.</li>', '<li>Paste with <kbd>⌘</kbd> + <kbd>V</kbd> and press <kbd>Enter</kbd>.</li>'),
 ('<li>설치가 끝나면 소복소복이 저절로 켜져요. <b>손쉬운 사용</b> 허용 창이 뜨면 소복소복을 켜 주세요. 그래야 Dock 위에도 눈이 쌓여요.</li>',
  '<li>Sobok starts by itself when the install finishes. If a window asks for <b>Accessibility</b> access, turn Sobok on. That lets snow pile up on the Dock too.</li>'),
 ('<p>화면 위쪽의 돋보기를 누르고 <b>소복소복</b>을 검색해서 클릭해요.</p>', '<p>Click the magnifying glass at the top of the screen, search for <b>Sobok</b>, and click it.</p>'),
 # 눈사람 만드는 법
 ('<h2 data-n="02">눈사람 만드는 법</h2>', '<h2 data-n="02">Build a snowman</h2>'),
 ('<b><em>01</em>눈덩이 뭉쳐서 굴리기</b> <span class="win"><kbd>Ctrl</kbd></span><span class="mac"><kbd>⌘</kbd></span> 을 누르고 쌓인 눈을 클릭하면 작은 눈덩이가 생겨요. 잡고 굴리면 점점 커져요. <small>(어디까지 커지려나..?)</small>',
  '<b><em>01</em>Pack it and roll it</b> Hold <span class="win"><kbd>Ctrl</kbd></span><span class="mac"><kbd>⌘</kbd></span> and click the snow to make a small snowball. Grab it and roll it, and it grows. <small>(How big can it get..?)</small>'),
 ('<b><em>02</em>차곡차곡 쌓기</b> 눈덩이 위에 눈덩이를 올려 주세요. 세 덩이면 눈사람 완성!', '<b><em>02</em>Stack them up</b> Put one snowball on top of another. Three makes a snowman!'),
 ('<b><em>03</em>말 걸어 보기</b> 눈사람을 콕 눌러 보세요. 별의별 소리를 다 해요.', '<b><em>03</em>Say hi</b> Give your snowman a poke. It has a lot to say.'),
 # 이런 것도 돼요
 ('<h2 data-n="03">이런 것도 돼요</h2>', '<h2 data-n="03">More to try</h2>'),
 ('<b>비율은 내 마음대로</b> 황금 비율? 그런게 어디있어요. 조금 요상하면 어때!', '<b>Any shape you like</b> Perfect proportions? No such thing. A little odd is fine!'),
 ('<b>친구를 만들어 주세요</b> 눈사람 둘을 나란히 세워 보세요. 조잘조잘 수다를 떨어요. 무슨 얘기 하는지는 직접 들어 보세요.', '<b>Make them a friend</b> Stand two snowmen side by side and they start chatting. Listen in to find out what about.'),
 ('<b>여기저기 데려다 놓기</b> 눈사람을 잡아서 옮길 수 있어요.<br>눈 쌓인 곳 어디든 올려 놓아요.', '<b>Take them anywhere</b> Grab a snowman and move it.<br>Set it down wherever there is snow.'),
 ('<b>조심히 다뤄주세요</b> 너무 세게 던지거나 높은 데서 떨어뜨리면 부서져요. <small><i>(약간 기분이 좋을 수도..?)</i></small>', '<b>Handle with care</b> Throw one too hard or drop it from too high and it breaks. <small><i>(Which might feel a little good..?)</i></small>'),
 ('<b>눈이 너무 많이 쌓이면?</b> 제설차가 와서 싹 치우고 가요.<br>열심히 만든 눈사람은 잘 지켜 드릴게요.', '<b>Too much snow?</b> A snowplow comes and clears it away.<br>Your snowmen stay safe.'),
 # 설정
 ('<h2 data-n="04">설정 바꾸기</h2>', '<h2 data-n="04">Settings</h2>'),
 ('화면에 <b>조그만 눈사람</b>이 숨어 있어요. 눌러 보면 설정 창이 열려요.', 'There is a <b>tiny snowman</b> hiding on your screen. Click it to open Settings.'),
 ('<p class="center">눈 내리는 양, 눈사람 말투, 말풍선 빈도와 글자 크기를<br>입맛대로 바꿀 수 있어요.</p>', '<p class="center">Change how much it snows, how the snowmen talk to you,<br>how often they talk, the text size, and the language.</p>'),
 ('<p class="hint">컴퓨터가 느려진다면 가볍게 모드를 켜 주세요.</p>', '<p class="hint">If your computer slows down, turn on Light mode.</p>'),
 # 지우기
 ('<h2 data-n="05">소복소복 지우기</h2>', '<h2 data-n="05">Uninstall</h2>'),
 ('<summary>지우는 방법 보기</summary>', '<summary>Show how to uninstall</summary>'),
 ('아쉽지만 소복소복을 떠나보내고 싶을 때는 아래 방법으로 삭제할 수 있어요.', 'Sad to see you go. This removes Sobok completely.'),
 ('<p><kbd>Windows 키</kbd> + <kbd>R</kbd> 을 누르고 아래 한 줄을 붙여 넣은 뒤 <kbd>Enter</kbd> 를 눌러요.</p>', '<p>Press the <kbd>Windows key</kbd> + <kbd>R</kbd>, paste the line below, and press <kbd>Enter</kbd>.</p>'),
 ('<p>터미널에 아래 한 줄을 붙여 넣고 <kbd>Enter</kbd> 를 눌러요.</p>', '<p>Paste the line below into Terminal and press <kbd>Enter</kbd>.</p>'),
 ('언젠가 또 눈사람이 보고 싶어지면 놀러 와요.', 'Come back whenever you miss the snowmen.'),
 # 꼬리
 ('마음에 드셨다면 <a href="https://github.com/lovejoohero0228/sobok">GitHub 에서 별 ⭐</a> 하나 눌러 주세요. 눈사람이 좋아해요.', 'If you like it, leave <a href="https://github.com/lovejoohero0228/sobok">a star ⭐ on GitHub</a>. The snowmen love that.'),
 ('  소복소복 · <a href="https://github.com/lovejoohero0228/sobok">소스 코드</a> · <a href="https://github.com/lovejoohero0228/sobok/issues/new">문제가 있나요?</a>',
  '  Sobok · <a href="https://github.com/lovejoohero0228/sobok">Source code</a> · <a href="https://github.com/lovejoohero0228/sobok/issues/new">Something wrong?</a> · <a href="../" hreflang="ko" lang="ko">한국어</a>'),
 ('문제를 알려 주실 때 기록 파일을 함께 보내 주시면 원인을 빨리 찾을 수 있어요.', 'If you report a problem, attaching the log file helps find the cause quickly.'),
 ("b.textContent = '복사됐어요!'", "b.textContent = 'Copied!'"),
 ('>복사하기</button>', '>Copy</button>'),
 # 파일 경로: 한 단계 아래 폴더에서 연다
 ('src="hero.mp4', 'src="../hero.mp4'), ('poster="hero.jpg"', 'poster="../hero.jpg"'), ('src="clips/', 'src="../clips/'),
]
for a, b in PAIRS: rep(a, b)
# 한국어 페이지에 달린 'English' 링크는 영어 페이지에서는 뺀다 (hreflang 표지는 원본에 이미 있다)
s = s.replace('<a href="#remove">Uninstall</a><a href="en/" hreflang="en" lang="en">English</a>', '<a href="#remove">Uninstall</a>')
rep(' · <a href="en/" hreflang="en" lang="en">English</a>', '')
# 메뉴 끝에 언어 전환
rep('<a href="#remove">Uninstall</a>', '<a href="#remove">Uninstall</a><a href="../" hreflang="ko" lang="ko">한국어</a>')

# 주석을 뺀 본문에 한글이 남았는지 본다 (언어 전환 링크와 이름 풀이는 빼고)
body = re.sub(r'<!--.*?-->', '', s, flags=re.S)
body = re.sub(r'/\*.*?\*/', '', body, flags=re.S)
body = re.sub(r'(?m)^\s*//.*$', '', body)
for ln in body.split('\n'):
    t = ln.replace('한국어', '').replace('소복소복 <i>(sobok-sobok)</i>', '')
    if re.search('[가-힣]', t): left.append(ln.strip()[:160])
os.makedirs('docs/en', exist_ok=True)
io.open('docs/en/index.html', 'w', encoding='utf-8', newline='\n').write(s)
print('written', len(s), 'chars; leftover Korean lines:', len(left))
for l in left: print('  ', l)
