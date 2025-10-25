class Card:
    def __init__(self, id: int, name: str, type: int, description: str, image_file: str, effect_tag: str, betting_value: int):
        self.id = id
        self.name = name
        self.type = type #메리트=1, 리스크=2, 패널티=3
        self.description = description
        self.effect_tag = effect_tag #player.effectlist에 추가할 내용
        self.image_file = image_file
        self.betting_value = betting_value

CARDS = [
    Card(
        id=1,
        name='느리구나, 쓰러지는 것 조차',
        type=1,
        description='플레이어 한명을 지정해, 그 플레이어의 속도를 1.0으로 내립니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=2,
        name="I'm fast fuck boy!",
        type=1,
        description='플레이어 한명을 지정해, 그 플레이어의 속도를 9.0으로 올립니다',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=3,
        name='bga는 감상하라고 있는거지',
        type=1,
        description='한 사람을 지정하면, 그 사람은 bga 밝기를 최대로 키우고 기어 투명도를 100%로 설정합니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=4,
        name='누구인가? 누가 기침소리를 내었어?',
        type=1,
        description='패널티 받는 사람을 고를 권리를 뺏어오고 각 기호가 누구인지 알 수 있게 됩니다. 만약 자신이 선곡자라면, 패널티 받는 사람을 한 명 더 선택 할 수 있습니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=5,
        name='안사요',
        type=1,
        description='즉시 자신에게 적용된 모든 부정적인 효과를 없앱니다. 만약 없앨 효과가 1개면 코인을 3개, 없으면 5개를 얻습니다.',
        effect_tag='',
        image_file='',
        betting_value=1
    ),
    Card(
        id=6,
        name='코인 사이에 "비트"코인',
        type=1,
        description='6코인을 획득합니다.',
        effect_tag='',
        image_file='',
        betting_value=0
    ),
    Card(
        id=7,
        name='소매넣기',
        type=1,
        description='(자신을 제외한)랜덤으로 1명을 뽑아 가산값 2를 적용합니다',
        effect_tag='',
        image_file='',
        betting_value=5
    ),
    Card(
        id=8,
        name='연쇄할인마',
        type=1,
        description='다음 찬스카드 구매가격이 2코인 감소합니다.',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=9,
        name='"줄"',
        type=1,
        description='이 카드를 가장 먼저 뽑은 플레이어에게 진행자가 [싸이버거 단품]을 선물합니다. 그 이후에 뽑은 플레이어에게는 대신 배팅 가산값을 5 줍니다.',
        effect_tag='',
        image_file='',
        betting_value=0
    ),
    Card(
        id=10,
        name='펀드는 무조건 오른다..!',
        type=2,
        description='펀드를 획득합니다. 펀드의 가치는 4코인 부터 시작하며, 라운드가 끝날 때 마다 1/2의 확률로 가치가 1코인 상승하거나 1코인 하락합니다.  원하는 타이밍에 언제든 팔 수 있습니다. 하지만, 가치가 0이된다면 펀드는 파기됩니다.',
        effect_tag='',
        image_file='',
        betting_value=0
    ),
    Card(
        id=11,
        name='주사위의 신',
        type=2,
        description='이 카드를 뽑는 즉시 코인 1개를 다시 받습니다. 6면 주사위를 한 번 돌린 뒤, 나온 숫자만큼 코인을 받습니다.',
        effect_tag='',
        image_file='',
        betting_value=0
    ),
    Card(
        id=12,
        name='25%픽업? 혜자잖아!',
        type=2,
        description='플레이어 1명을 몰래 지정합니다. 지정된 플레이어가 다음 라운드의 라운드 페널티를 받으면 본인은 3코인을 받습니다',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=13,
        name='디맥에서 가장 재미있는 키가 뭐라고?',
        type=2,
        description='디맥에서 가장 재미있다고 생각하는 키를 크게 외칩니다. 만약 그 키가 5b나 8b라면 배팅을 4 가산하고, 4b나 6b라면 당신의 신념에 모두가 박수를 칩니다.',
        effect_tag='',
        image_file='',
        betting_value=0
    ),
    Card(
        id=14,
        name='공산당',
        type=2,
        description='찬스카드를 결과를 보지 않고 하나 더 뽑습니다. 결과를 다른 플레이어들에게 먼저 보여줍니다. 반응을 보고 찬스카드를 적용 할 지 안할지 결정합니다. 만일, 적용하지 않기로 했다면, 찬스카드를 추가로 뽑고 적용하기로 할 때 까지 반복합니다.',
        effect_tag='',
        image_file='',
        betting_value=0
    ),
    Card(
        id=15,
        name='사.돌.조.아',
        type=2,
        description='플레이 중 디코방에 Show time 이 울려퍼집니다',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=16,
        name='너의 군생활',
        type=2,
        description='모니터를 끄거나, 눈을 감고 플레이합니다.',
        effect_tag='',
        image_file='',
        betting_value=10
    ),
    Card(
        id=17,
        name='단체로 에어웨이브치다 혼절',
        type=2,
        description='이번 라운드 선곡이 airwave ~extended mix~ 4BMX로 변경됩니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=18,
        name='한컴 타자연습',
        type=2,
        description='카드를 뽑은 플레이어의 난이도를 노말로 고정합니다. 해당 플레이어의 모든 키배치(사이드 포함)를 a~z중 랜덤으로 뽑아 원하는 라인에 배치합니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=19,
        name='쫄?',
        type=2,
        description='본인의 기존 속도에서 속도를 얼마나 올릴지[낮출지] 정합니다. (변화량/2)만큼 베팅을 가산합니다. (소수점 둘째자리에서 반올림). 이 효과가 발동된 라운드는 속도를 강제로 변화시키는 효과가 무효가 됩니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=20,
        name='선호패턴 : 연타',
        type=2,
        description='본인에게 맥스랜덤을 적용합니다.',
        effect_tag='',
        image_file='',
        betting_value=5
    ),
    Card(
        id=21,
        name='안구건조증 예방',
        type=2,
        description='모두가 블링크2 옵션을 적용합니다',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=22,
        name='용의 눈으로 봐라',
        type=2,
        description='모두 블라인드를 적용합니다. (노트스킨과 기어는 자유롭게 바꾸셔도 좋습니다.)',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=23,
        name='허허 개판이네',
        type=2,
        description='모든 플레이어는 배치변경, 페이더, 카오스를 모두 적용합니다. 이미 적용되어있는게 있다면 바꾸지 않습니다. 적용할 효과들은 룰렛으로 정합니다. 각각의 효과들은 독립적인 부정적인 효과로 간주합니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=24,
        name='죄수의 딜레마',
        type=2,
        description='다른 플레이어 하나를 지목합니다. 당신과 그 플레이어의 점수가 모두 0점이라면 둘 모두 퍼펙트 처리됩니다. 만일 한 플레이어가 0점이고, 다른 플레이어의 점수가 0점이 아니라면 0점이 아닌 플레이어는  1250000점 처리되고, 0점인 플레이어는 700000점 처리됩니다. 만일 둘다 0점이 아니라면, 둘 모두 점수가 900000점 처리됩니다. 이 효과는, 점수에 영향을 주는 다른 효과가(77.77% 등) 적용되어있었거나 적용된다면 무효처리 됩니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=25,
        name='77.77%',
        type=2,
        description='500000점 이상 800000점 이하의 타깃 스코어를 설정합니다. 모든 플레이어의 이번 라운드의 게임 결과 점수는 1000000-(타깃 스코어와 실제 스코어의 오차)가 됩니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=26,
        name='진짜 베팅',
        type=2,
        description='이번 라운드는 진행자만 플레이합니다. 진행자의 점수를 미리 예측하고, 예측이 가장 가까운 순서대로 100만,90만,80만,70만,60만...의 점수를 획득합니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=27,
        name='B보M묵K가위 초대 우승자',
        type=2,
        description='이번 라운드의 게임이 끝나고 가위바위보를 합니다. 모든 플레이어는 가위바위보를 해서 순위대로 원하는 플레이어의 점수를 자신의 점수로 적용할 수 있습니다. 이미 선택된 대상은 선택할 수 없습니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=28,
        name='레이튼 교수와 멍청한 조수',
        type=2,
        description='진행자가 게임 도중 문제(상식퀴즈 등)를 출제합니다. 가장 먼저 정답을 맞춘 플레이어는 200000점을 이번 플레이 결과에 가산합니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=29,
        name='GET READY FOR THE NEXT BATTLE',
        type=2,
        description='(자신을 포함한) 플레이어 중 두명을 지목합니다. 둘은 라운드가 시작하기 전 버서스(키와 티어는 카드 사용자가 선택)를 진행합니다. 승리한 플레이어는 패배한 플레이어에게 이번 라운드 점수 50000점을 빼앗아 옵니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=30,
        name='콩진호가 간다! 콩진호가 간다!',
        type=2,
        description='모든 플레이어의 이번 라운드의 점수결과에 숫자 "2" 한 개 마다 22222점을 결과에 가산합니다. 추가적으로, 모든 플레이어의 이번 라운드의 점수결과에 숫자 "2" 한 개 마다 22222점을 결과에 가산합니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=31,
        name='🙏🙏🙏',
        type=2,
        description='이모티콘을 한 번 쓸 때마다 3500점 씩 획득합니다.(피버 이모티콘 제외)',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=32,
        name='지옥의 이지선다',
        type=2,
        description='다른 플레이어 하나를 몰래 지정합니다. 게임 플레이 후에, 대상인 플레이어를 공개하고 50%의 확률로 그 플레이어와 내 점수가 바뀝니다. 만약 다른 점수카드와 중복이 된다면, 큐피드의 화살 적용 직전에 적용됩니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=33,
        name='큐피트의 화살',
        type=2,
        description='다른 플레이어 하나를 지목합니다. 당신과 그 플레이어의 이번 라운드의 플레이 결과는 둘의 평균값이 됩니다. 이 카드는 다른 모든 점수관련 효과가 적용된 후 마지막에 적용됩니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=34,
        name='홀짝',
        type=2,
        description='카드를 뽑은 플레이어가 홀/짝 중 하나를 정합니다. 게임이 끝나고 코인 배수 적용 직전의 자신의 점수의 홀수 또는 짝수를 맟추면 1코인을 받습니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=35,
        name='그래도 너보단 내가',
        type=2,
        description='모든 플레이어가 0~7의 숫자 중, 하나를 동시에 고릅니다. 숫자가 가장 높은 1명을 제외하고, 모두 고른 숫자만큼의 코인을 획득합니다.',
        effect_tag='',
        image_file='',
        betting_value=0
    ),
    Card(
        id=36,
        name='누구게?',
        type=2,
        description='진행자는 사전에 받은 참가자 본인 것을 제외한 친구코드(진행자 포함) 중에 하나를 아무거나 이야기 합니다. 이 카드를 뽑은 사람은 그것이 누구의 친구코드인지 맞추면, 배팅 가산값이 3 상승합니다.',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=37,
        name='국민연금',
        type=2,
        description='이번 라운드 시작 직전에 베팅 가산값이 0이 됩니다. 다음 라운드 시작 직전에 베팅 가산값이 (없앤 배팅 가산값+(1D6-3))만큼 증가합니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=38,
        name='빙빙 돌아가는 돌림판',
        type=2,
        description='돌림판을 돌려 나온 배팅 가산값을 더합니다. (+2 1개, +3 2개, +4 5개, +5 2개, +7 1개, +9 1개: 기댓값 4.5)',
        effect_tag='',
        image_file='',
        betting_value=0
    ),
    Card(
        id=39,
        name='따서 갚으면 된다니까???',
        type=2,
        description='이 카드를 뽑은 플레이어는 자신의 코인으로 진행자와 블랙잭을 진행합니다. 최대 배팅액은 5코인이며, 5판 진행하여 진행자를 3판 이상 이겼을 시 두배로 받습니다. (스플릿, 더블다운 등의 기타 블랙잭 룰은 전부 사용하지 않습니다.)',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=40,
        name='훌륭한 선동가',
        type=2,
        description='2분간, 자신이 배팅 가산값을 3보다 더 받아야 할 이유를 연설합니다. 연설이 끝나고, 모든 플레이어가 [준다]/[안준다]를 각자 투표합니다. 결과의 [준다] 한 표당 배팅 가산값을 +1합니다.',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=41,
        name='내가 아는 너는 이렇지 않았는데',
        type=2,
        description='다른 플레이어 하나를 지정합니다. 그 플레이어는 자신의 "진짜\'리듬게임 성과 하나와, "가짜"성과 두개를 선택하여 제시합니다. (어떤 리듬게임이든 무관) 카드를 뽑은 플레이어는 이 중 하나를 골라 "진짜"성과였다면, 배팅 가산값을 +4 합니다.',
        effect_tag='',
        image_file='',
        betting_value=2
    ),
    Card(
        id=42,
        name='아니 그니까',
        type=2,
        description='다른 플레이어 하나를 지정합니다. 진행자가 이 카드를 뽑은 플레이어에게 단어 하나를 제시합니다. 게임이 진행돼는 동안, 이 단어를 지정한 플레이어에게 설명합니다. 게임이 끝나기 전까지, 지정한 플레이어가 단어를 맞추는데 성공하면 둘 모두 결과에 150000점을 가산합니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
    Card(
        id=43,
        name='원-핸드 마스터',
        type=2,
        description='이번 라운드는 한 손으로 플레이합니다. 오른손일지 왼손일지는 룰렛으로 결정합니다.',
        effect_tag='',
        image_file='',
        betting_value='직접해봐야알듯'
    ),
    Card(
        id=44,
        name='나는 자랑스러운 태극기 아래',
        type=3,
        description='애국가를 틀어놓고 플레이 합니다( https://www.youtube.com/watch?v=_fhRBvbTXDI )',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=45,
        name='고요를 체험하시오',
        type=3,
        description='마스터 볼륨을 0으로 설정하고 플레이합니다.',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=46,
        name='핑이 좀 튀네',
        type=3,
        description='판정 타이밍을 최대치로 설정합니다',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=47,
        name='모니터가 너무 작아요',
        type=3,
        description='640×360 해상도와  Windows디스플레이모드를 적용합니다.',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=48,
        name='커서 피펨즈가 될래요!',
        type=3,
        description='리버스를 적용합니다',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=49,
        name='말랑말랑한 뇌',
        type=3,
        description='Chaos X를 적용합니다.',
        effect_tag='',
        image_file='',
        betting_value=3
    ),
    Card(
        id=50,
        name='인플레이션',
        type=3,
        description='다음 찬스카드 구매가격이 1코인 상승합니다.',
        effect_tag='',
        image_file='',
        betting_value=4
    ),
]