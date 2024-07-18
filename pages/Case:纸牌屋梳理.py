import streamlit as st
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from camel.configs import ChatGPTConfig
from agents import InsightAgent

st.title("Case: 纸牌屋梳理")

st.image('case1.png', caption='Knowledge Graph for House of Cards')

# Sidebar for API Key input
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password') or st.secrets["OPENAI_KEY"]

st.info("""Based on the relationship information provided, here are some insights:

1. **Creation and Adaptation**:
   - "House of Cards" was created by Beau Willimon and is based on the 1989 novel. It is an adaptation of the 1990 British series and was released on Netflix, produced by the studio.

2. **Setting and Main Characters**:
   - The series is set in Washington, D.C., with Frank Underwood as the main character, portrayed by Kevin Spacey. Frank is affiliated with the Democratic Party and represents South Carolina's 5th congressional district. He is married to Claire Underwood, portrayed by Robin Wright.

3. **Awards and Recognition**:
   - "House of Cards" has received a Primetime Emmy Award and a Golden Globe Award. Kevin Spacey and Robin Wright have both won Golden Globe Awards for their roles.

4. **Political Ambitions and Positions**:
   - Frank Underwood holds the position of House Majority Whip and was denied the appointment of Secretary of State. He eventually becomes the Vice President and later the President of the United States. Claire Underwood also holds significant positions, including U.S. Ambassador to the United Nations and eventually becomes the President.

5. **Relationships and Conflicts**:
   - Frank and Claire Underwood have a complex relationship, involving both collaboration and conflict. Frank manipulates and undermines various political figures, including President Garrett Walker and Raymond Tusk. Claire faces crises and conflicts with figures like Russian President Viktor Petrov.

6. **Manipulation and Power Struggles**:
   - Frank Underwood is involved in numerous manipulative and power-driven actions, including conspiring behind the President, manipulating Peter Russo, and engaging in back-channel negotiations. He also uses the ICO crisis as a pretext to enact martial law and consolidate polling places.

7. **Investigations and Threats**:
   - Frank and Claire Underwood face investigations from various characters, including Zoe Barnes, Lucas Goodwin, and Tom Hammerschmidt. Frank is threatened by Hammerschmidt's campaign and impeachment hearings.

8. **Final Power Dynamics**:
   - Claire Underwood ultimately becomes the President of the United States, with significant influence and power struggles involving the Shepherds, Doug Stamper, and other political figures. The series ends with Claire suffocating Doug Stamper, solidifying her control.

These insights highlight the intricate web of relationships, power struggles, and political maneuvers that define "House of Cards.""")

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')

if openai_api_key:

    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O,
        model_config_dict=ChatGPTConfig().__dict__,
        api_key=openai_api_key
    )

    insight_agent = InsightAgent(model=model)  # Initialize the insight_agent here

    with st.form('my_form'):
        text_query = st.text_area('Enter query:', "What platform did House of Cards released?")
        submitted = st.form_submit_button('Submit Query')

        if submitted:
            ans = insight_agent.run(
                relationship_info="""
   Subject: House of Cards, Object: Beau Willimon, Type: CreatedBy
   Subject: House of Cards, Object: 1989 novel, Type: BasedOn
   Subject: House of Cards, Object: 1990 British series, Type: AdaptationOf
   Subject: House of Cards, Object: Netﬂix, Type: ReleasedOn
   Subject: Netﬂix, Object: Studio, Type: ProducedBy
   Subject: House of Cards, Object: Washington, D.C., Type: SetIn
   Subject: House of Cards, Object: Frank Underwood, Type: MainCharacter
   Subject: Frank Underwood, Object: Kevin Spacey, Type: PortrayedBy
   Subject: Frank Underwood, Object: Democrat, Type: AffiliatedWith
   Subject: Frank Underwood, Object: South Carolina\'s 5th congressional district, Type: Represents
   Subject: Frank Underwood, Object: Claire Underwood, Type: MarriedTo
   Subject: Claire Underwood, Object: Robin Wright, Type: PortrayedBy
   Subject: Frank Underwood, Object: Secretary of State, Type: DeniedAppointment
   Subject: Frank Underwood, Object: House Majority Whip, Type: CurrentPosition
   Subject: House of Cards, Object: Primetime Emmy Award, Type: Received
   Subject: House of Cards, Object: Golden Globe Award, Type: Earned
   Subject: Primetime Emmy Award, Object: Outstanding Drama Series, Type: Nominated for
   Subject: Primetime Emmy Award, Object: Outstanding Lead Actor, Type: Nominated for
   Subject: Primetime Emmy Award, Object: Outstanding Lead Actress, Type: Nominated for
   Subject: Golden Globe Award, Object: Robin Wright, Type: Won for
   Subject: Golden Globe Award, Object: Kevin Spacey, Type: Won for
   Subject: Kevin Spacey, Object: Television Series Drama, Type: WonAward
   Subject: Kevin Spacey, Object: 2015, Type: WonAwardYear
   Subject: Kevin Spacey, Object: Netflix, Type: WorkedWith
   Subject: Kevin Spacey, Object: Actor, Type: Occupies
   Subject: Season 1, Object: Kevin Spacey, Type: FeaturedIn
   Subject: Frank Underwood, Object: South Carolina, Type: Represents
   Subject: Frank Underwood, Object: House majority whip, Type: HoldsPosition
   Subject: Frank Underwood, Object: President Garrett Walker, Type: Supports
   Subject: Frank Underwood, Object: Secretary of State, Type: ExpectedPosition
   Subject: President Garrett Walker, Object: Congress, Type: Leads
   Subject: d, Object: President, Type: ConspiresBehind
   Subject: Claire, Object: NGO, Type: Runs
   Subject: Claire, Object: Clean Water Initiative, Type: Uses
   Subject: Claire, Object: Underwood, Type: WorksWith
   Subject: Frank, Object: Claire, Type: MarriedTo
   Subject: Frank, Object: Claire, Type: SchemesWith
   Subject: Frank, Object: Remy Danton, Type: WorksWith
   Subject: Claire, Object: Remy Danton, Type: WorksWith
   Subject: John, Object: XYZ Corporation, Type: WorksAt
   Subject: John, Object: New York City, Type: ResidesIn
   Subject: Underwood, Object: Zoe Barnes, Type: RomanticInvolvement
   Subject: Underwood, Object: Peter Russo, Type: Manipulates
   Subject: Underwood, Object: Walker, Type: Undermines
   Subject: Underwood, Object: Senator Michael Kern, Type: Opposes
   Subject: Underwood, Object: Senator Catherine Durant, Type: Replaces
   Subject: Underwood, Object: Walker, Type: ImprovesStandingWith
   Subject: Underwood, Object: Vice President, Type: IsFormerOf
   Subject: Vice President, Object: special election, Type: LeadsTo
   Subject: special election, Object: successor, Type: ResultsIn
   Subject: Underwood, Object: Russo, Type: Helps
   Subject: Underwood, Object: Rachel Posner, Type: UsesToTrigger
   Subject: Russo, Object: Underwood, Type: DecidesToExpose
   Subject: Underwood, Object: Russo, Type: Kills
   Subject: Underwood, Object: Vice President, Type: Convinces
   Subject: Vice President, Object: Governor, Type: StepsDown
   Subject: Governor, Object: Vice Presidency, Type: LeavesOpen
   Subject: Underwood, Object: Vice Presidency, Type: Plans
   Subject: Underwood, Object: Missouri, Type: IntroducedTo
   Subject: Underwood, Object: Raymond Tusk, Type: IntroducedTo
   Subject: Raymond Tusk, Object: Walker, Type: RevealsInfluence
   Subject: Raymond Tusk, Object: Walker, Type: Convinces
   Subject: Raymond Tusk, Object: Walker, Type: ExplainsInfluence
   Subject: Underwood, Object: Tusk, Type: Negotiates
   Subject: Underwood, Object: Tusk, Type: Collaborates
   Subject: Zoe, Object: Underwood, Type: Investigates
   Subject: Underwood, Object: Vice President of the United States, Type: Accepts Nomination
   Subject: Zoe, Object: Frank, Type: Investigates
   Subject: Lucas Goodwin, Object: Frank, Type: Investigates
   Subject: Janine Skorsky, Object: Frank, Type: Investigates
   Subject: Frank, Object: Rachel, Type: Locates
   Subject: Doug Stamper, Object: Rachel, Type: Protects
   Subject: Frank, Object: Zoe, Type: Lures
   Subject: Janine, Object: Zoe, Type: Investigates
   Subject: Lucas, Object: Zoe, Type: ContinuesSearch
   Subject: Lucas, Object: Gavin Orsay, Type: SeeksHelp
   Subject: Gavin Orsay, Object: Doug, Type: WorksFor
   Subject: Gavin Orsay, Object: Lucas, Type: FramesForCyberterrorism
   Subject: Gavin Orsay, Object: Rachel, Type: Extorts
   Subject: Rachel, Object: Doug, Type: Ambushes
   Subject: him, Object: dead, Type: FleesInto
   Subject: him, Object: hiding, Type: FleesInto
   Subject: Frank, Object: Claire, Type: Spouse
   Subject: Claire, Object: First Lady, Type: Friend
   Subject: Claire, Object: Walker, Type: Friend
   Subject: Walker, Object: Tusk, Type: Colleague
   Subject: Frank, Object: Walker, Type: Opponent
   Subject: Frank, Object: Tusk, Type: Opponent
   Subject: Frank, Object: Xander Feng, Type: Acquaintance
   Subject: Xander Feng, Object: Tusk, Type: Ally
   Subject: Frank, Object: back-channel negotiations, Type: EngagesIn
   Subject: Frank, Object: Tusk, Type: Undermines
   Subject: Tusk, Object: China, Type: Opposes
   Subject: Tusk, Object: Walker, Type: Opposes
   Subject: Tusk, Object: trade war, Type: ResultsIn
   Subject: Tusk, Object: tribal casino, Type: Owns
   Subject: Frank, Object: Feng, Type: Discovery
   Subject: Frank, Object: Republican PACs, Type: MoneyFlow
   Subject: Feng, Object: Tusk, Type: Partnership
   Subject: Feng, Object: Republican PACs, Type: Donations
   Subject: Feng, Object: Tusk, Type: EndPartnership
   Subject: Feng, Object: Long Island Sound, Type: Contract
   Subject: Justice Department, Object: White House, Type: Investigates
   Subject: White House, Object: Feng, Type: HasTiesWith
   Subject: White House, Object: Tusk, Type: HasTiesWith
   Subject: Frank, Object: Walker, Type: Manipulates
   Subject: Walker, Object: marriage counselor, Type: Visits
   Subject: Walker, Object: White House Counsel, Type: Coaches
   Subject: House Judiciary Committee, Object: Walker, Type: DraftsArticlesOfImpeachment
   Subject: special prosecutor, Object: White House Counsel, Type: Interprets
   Subject: Walker, Object: Frank, Type: OfferPardon
   Subject: Walker, Object: Tusk, Type: OfferPardon
   Subject: Tusk, Object: Walker, Type: TestifiesAgainst
   Subject: Walker, Object: Tusk, Type: DealCancelled
   Subject: Walker, Object: Frank, Type: RegainTrust
   Subject: Walker, Object: Tusk, Type: DealCancelled
   Subject: Walker, Object: Frank, Type: SwornInAs
   Subject: Frank Underwood, Object: America Works, Type: Proposes
   Subject: Frank Underwood, Object: President, Type: Holds
   Subject: Frank Underwood, Object: 2016 election, Type: CompetesIn
   Subject: Heather Dunbar, Object: Democratic primaries, Type: CompetesAgainst
   Subject: Claire, Object: U.S. Ambassador, Type: HoldsPosition
   Subject: Claire, Object: United Nations, Type: WorksAt
   Subject: Claire, Object: Jordan Valley, Type: FacesCrisis
   Subject: Claire, Object: Frank, Type: PittedAgainst
   Subject: Claire, Object: Russian President Viktor Petrov, Type: PittedAgainst
   Subject: Russian President Viktor Petrov, Object: American gay rights activist, Type: HasArrested
   Subject: Underwoods, Object: Russian President Viktor Petrov, Type: Persuade
   Subject: Russian President Viktor Petrov, Object: American gay rights activist, Type: DemandsRelease
   Subject: American gay rights activist, Object: Russian television, Type: ApologizeOn
   Subject: American gay rights activist, Object: Claire, Type: VisitedBy
   Subject: American gay rights activist, Object: Russian television, Type: ApologizeOn
   Subject: American gay rights activist, Object: Russian television, Type: KillHimself
   Subject: Russian troops, Object: Jordan Valley, Type: AreKilledBy
   Subject: Russian President Viktor Petrov, Object: Jordan Valley, Type: IncidentInvolving
   Subject: Frank, Object: Claire, Type: Influences
   Subject: Frank, Object: Ambassador, Type: RequestsRemoval
   Subject: Claire, Object: Ambassador, Type: Resigns
   Subject: Claire, Object: Frank, Type: DesireToBeActive
   Subject: Frank, Object: Doug, Type: RefusesToReinstate
   Subject: Doug, Object: Dunbar, Type: SwitchesSides
   Subject: Gavin, Object: Doug, Type: HelpsTrackDown
   Subject: Gavin, Object: Rachel, Type: DeliversFindings
   Subject: Doug, Object: Gavin, Type: Brutalizes
   Subject: Doug, Object: Rachel, Type: Kills
   Subject: Doug, Object: New Mexico, Type: FindsLivingLocation
   Subject: Doug, Object: Chief of Staff, Type: ReturnsToWork
   Subject: Peter Remy, Object: Company, Type: ResignsFrom
   Subject: Thomas Yates, Object: Frank, Type: HiredBy
   Subject: Thomas Yates, Object: America Works, Type: Promotes
   Subject: Thomas Yates, Object: Claire, Type: WritesAbout
   Subject: Thomas Yates, Object: Frank, Type: WritesAbout
   Subject: Thomas Yates, Object: Frank, Type: Reads
   Subject: Thomas Yates, Object: Frank, Type: Agrees
   Subject: Thomas Yates, Object: Frank, Type: WritesChapter
   Subject: book, Object: Yates, Type: Fires
   Subject: Underwoods, Object: Claire, Type: TensionsBetween
   Subject: Underwoods, Object: Frank, Type: TensionsBetween
   Subject: Claire, Object: Frank, Type: IntentToLeave
   Subject: Season 4, Object: 2016, Type: ReleasedIn
   Subject: Claire, Object: Dallas, Type: RelocatesTo
   Subject: Claire, Object: Congress, Type: RunsFor
   Subject: Doris Jones, Object: Celia, Type: Endorses
   Subject: Claire, Object: Planned Parenthood clinic, Type: OffersFunding
   Subject: Doris Jones, Object: Celia, Type: PlansSuccessor
   Subject: Frank, Object: Claire, Type: WinsBackSupport
   Subject: Frank, Object: Texas, Type: PromisesNotToSabotage
   Subject: Frank, Object: Celia, Type: EndorsesIn
   Subject: Frank, Object: State of the Union address, Type: PubliclyEndorses
   Subject: Frank, Object: South Carolina, Type: TravelsTo
   Subject: Frank, Object: Dunbar, Type: LosesTo
   Subject: Frank, Object: Claire, Type: DiscoversLeaking
   Subject: Dunbar, Object: Frank, Type: Threatens
   Subject: Frank, Object: Dunbar, Type: Refuses
   Subject: Lucas Goodwin, Object: Frank, Type: SeeksRevengeAgainst
   Subject: Lucas Goodwin, Object: Zoe Barnes, Type: Killed
   Subject: Lucas Goodwin, Object: Dunbar, Type: ExplainsStoryTo
   Subject: Lucas Goodwin, Object: Frank, Type: AttemptsToAssassinate
   Subject: Lucas Goodwin, Object: Edward Meechum, Type: Kills
   Subject: Edward Meechum, Object: Lucas Goodwin, Type: FatallyWounds
   Subject: Frank, Object: Edward Meechum, Type: SeverelyWoundedBy
   Subject: Frank, Object: United States, Type: RemainsComatoseIn
   Subject: Donald Blythe, Object: United States, Type: SwornInAsActingPresidentOf
   Subject: Frank, Object: Claire, Type: MarriedTo
   Subject: Frank, Object: Blythe, Type: Consults
   Subject: Claire, Object: Blythe, Type: Convinces
   Subject: Claire, Object: China, Type: Involves
   Subject: Claire, Object: Petrov, Type: Meets
   Subject: Claire, Object: Doug, Type: LeakInformation
   Subject: Doug, Object: Dunbar, Type: RevealsMeeting
   Subject: Dunbar, Object: Lucas, Type: SecretMeetingWith
   Subject: Frank, Object: Dunbar, Type: ForcesSuspension
   Subject: Frank, Object: Claire, Type: PutsOnTicket
   Subject: Tom Hammerschmidt, Object: Zoe, Type: FormerNewsEditorOf
   Subject: Tom Hammerschmidt, Object: Lucas, Type: FormerNewsEditorOf
   Subject: Tom Hammerschmidt, Object: Frank, Type: Investigates
   Subject: Tom Hammerschmidt, Object: Remy Danton, Type: CollaboratesWith
   Subject: Tom Hammerschmidt, Object: Walker, Type: Convinces
   Subject: Remy Danton, Object: Frank, Type: RevealsCorruptionOf
   Subject: Jackie Sharp, Object: Frank, Type: Opposes
   Subject: American family, Object: Tennessee, Type: KidnappedIn
   Subject: KidnappedIn, Object: Islamist group, Type: BySupportersOf
   Subject: Frank, Object: Islamic Caliphate Organization (ICO), Type: NegotiatesWith
   Subject: Frank, Object: Governor Will Conway, Type: InvitesToAssist
   Subject: Governor Will Conway, Object: White House, Type: Visits
   Subject: Frank, Object: Claire, Type: MarriedTo
   Subject: Frank, Object: kidnappers, Type: AllowsCommunicationWith
   Subject: Claire, Object: Frank, Type: MarriedTo
   Subject: kidnappers, Object: leader of ICO, Type: CommunicatesWith
   Subject: leader of ICO, Object: Yusuf al Ahmadi, Type: SamePersonAs
   Subject: leader of ICO, Object: hostages, Type: Holds
   Subject: Yusuf al Ahmadi, Object: kidnappers, Type: Urges
   Subject: Yusuf al Ahmadi, Object: hostages, Type: Urges
   Subject: Hammerschmidt, Object: Frank, Type: Threatens
   Subject: Hammerschmidt, Object: Frank, Type: ThreatensCampaign
   Subject: Frank, Object: Hammerschmidt, Type: ThreatenedBy
   Subject: Claire, Object: Frank, Type: Urges
   Subject: Claire, Object: Frank, Type: DecidesWith
   Subject: Frank, Object: nation, Type: Declares
   Subject: Frank, Object: military, Type: Orders
   Subject: Frank, Object: global terrorism, Type: CombatAgainst
   Subject: Frank, Object: hostage, Type: WatchesExecutionWith
   Subject: Claire, Object: Frank, Type: WatchesExecutionWith
   Subject: Claire, Object: Frank, Type: BreakingTheFourthWall
   Subject: Frank, Object: ICO, Type: UsesAsPretext
   Subject: Frank, Object: martial law, Type: Enacts
   Subject: Frank, Object: urban areas, Type: EnactsIn
   Subject: Frank, Object: polling places, Type: Consolidates
   Subject: Frank, Object: Democratic governors, Type: CollaboratesWith
   Subject: Democratic governors, Object: safety, Type: OfficialReason
   Subject: Doug, Object: hacker Aidan Macallan, Type: Blackmails
   Subject: hacker Aidan Macallan, Object: cyberattack, Type: Launches
   Subject: cyberattack, Object: NSA, Type: On
   Subject: cyberattack, Object: Internet, Type: SlowsDown
   Subject: Underwood Administration, Object: ICO, Type: Blames
   Subject: Underwood Administration, Object: Election Day, Type: HingesOn
   Subject: Election Day, Object: Pennsylvania, Type: HingesOn
   Subject: Election Day, Object: Tennessee, Type: HingesOn
   Subject: Election Day, Object: Ohio, Type: HingesOn
   Subject: Conway, Object: Pennsylvania, Type: Secures
   Subject: Conway, Object: Ohio, Type: SeemsToSwing
   Subject: Underwood Administration, Object: Knoxville, Type: StagesTerroristAttack
   Subject: Knoxville, Object: ICO, Type: PinnedOn
   Subject: Underwoods, Object: Ohio Governor, Type: Contacted
   Subject: Ohio Governor, Object: Ohio, Type: ClosedPolls
   Subject: Ohio, Object: Tennessee, Type: RefusedToCertify
   Subject: Twelfth Amendment, Object: Congress, Type: Invoke
   Subject: Conway, Object: Congress, Type: Meeting
   Subject: Conway, Object: Frank, Type: Rivalry
   Subject: Conway, Object: House, Type: Tie
   Subject: Claire, Object: Senate, Type: Secure
   Subject: Claire, Object: United States, Type: ActingPresident
   Subject: Frank Underwood, Object: Claire Underwood, Type: Spouse
   Subject: Frank Underwood, Object: Jane Davis, Type: CollaboratesWith
   Subject: Frank Underwood, Object: Ohio, Type: CampaignsIn
   Subject: Frank Underwood, Object: Tennessee, Type: CampaignsIn
   Subject: Jane Davis, Object: Commerce Department, Type: WorksAt
   Subject: Frank Underwood, Object: Elysian Fields, Type: AttendsMeetingAt
   Subject: Conway, Object: Ohio, Type: MentalBreakdownIn
   Subject: Frank Underwood, Object: Leaked Information, Type: InvolvedInLeak
   Subject: Claire Underwood, Object: Leaked Information, Type: InvolvedInLeak
   Subject: Leaked Information, Object: Media, Type: RevealedToMedia
   Subject: Will Conway, Object: Mark Usher, Type: ManagedBy
   Subject: Frank, Object: Underwoods, Type: BelongsTo
   Subject: Claire, Object: Underwoods, Type: BelongsTo
   Subject: Frank, Object: Ohio, Type: WinsElectionIn
   Subject: Frank, Object: Tennessee, Type: WinsElectionIn
   Subject: Frank, Object: President, Type: SwornInAs
   Subject: Claire, Object: Vice President, Type: SwornInAs
   Subject: Hammerschmidt, Object: Zoe, Type: Investigates
   Subject: Hammerschmidt, Object: White House, Type: Leaker
   Subject: Hammerschmidt, Object: Frank, Type: ImpeachmentHearing
   Subject: Underwoods, Object: White House, Type: Surveillance
   Subject: Leaker, Object: Hammerschmidt, Type: Informs
   Subject: Leaker, Object: Doug, Type: Implicates
   Subject: Underwoods, Object: Doug, Type: Convinces
   Subject: Frank, Object: Zoe, Type: Killed
   Subject: Frank, Object: Frank, Type: Leaked
   Subject: Frank, Object: Claire, Type: ResignsTo
   Subject: Frank, Object: Claire, Type: WorksAlongside
   Subject: Frank, Object: Secretary Durant, Type: PushesDown
   Subject: Claire, Object: Yates, Type: PoisonsWith
   Subject: Gelsemium, Object: Jane, Type: ProvidedTo
   Subject: Gelsemium, Object: contractors, Type: ConcernedAbout
   Subject: contractors, Object: Underwoods, Type: WorkingFor
   Subject: Underwoods, Object: LeAnn, Type: Eliminate
   Subject: LeAnn, Object: car, Type: RammingOffRoad
   Subject: car, Object: guard rail, Type: Into
   Subject: Frank, Object: president, Type: ResignsAs
   Subject: Frank, Object: Claire, Type: Leaving
   Subject: Claire, Object: United States, Type: BecomesPresidentOf
   Subject: Claire, Object: Frank, Type: Pardon
   Subject: military special operations unit, Object: ICO, Type: TakingOutLeaderOf
   Subject: media focus, Object: Frank, Type: MovesAwayFrom
   Subject: Claire, Object: Oval Office, Type: StandingIn
   Subject: Claire, Object: Frank, Type: ReconsiderPardon
   Subject: Claire, Object: Frank, Type: IgnoreCalls
   Subject: Claire, Object: Viewers, Type: BreakFourthWall
   Subject: Season 6, Object: 2018, Type: ReleasedIn
   Subject: Claire, Object: Bill Shepherd, Type: Influence
   Subject: Claire, Object: Annette Shepherd, Type: Influence
   Subject: Bill Shepherd, Object: Annette Shepherd, Type: FamilyRelation
   Subject: Bill Shepherd, Object: Mark Usher, Type: Connection
   Subject: Annette Shepherd, Object: Mark Usher, Type: Affair
   Subject: Annette Shepherd, Object: Duncan, Type: FamilyRelation
   Subject: Duncan, Object: Claire, Type: Pressure
   Subject: Duncan, Object: Gardner Analytics, Type: Ownership
   Subject: Claire, Object: Shepherds, Type: Embarrasses
   Subject: Shepherds, Object: Claire, Type: Opposes
   Subject: Doug, Object: psychiatrist, Type: InTherapy
   Subject: Claire, Object: Assistant Director Green, Type: Monitors
   Subject: The Shepherds, Object: Claire, Type: Influence
   Subject: The Shepherds, Object: Supreme Court justice, Type: Convince
   Subject: The Shepherds, Object: Seth Grayson, Type: Collaborate
   Subject: The Shepherds, Object: mobile application, Type: Develop
   Subject: mobile application, Object: user\'s activity, Type: Monitor
   Subject: Secretary of State Durant, Object: prosecutors, Type: Communicate
   Subject: The Shepherds, Object: Secretary of State Durant, Type: Persuade
   Subject: The Shepherds, Object: Underwoods, Type: Distance
   Subject: Claire, Object: Jane Davis, Type: PlotToAssassinate
   Subject: Claire, Object: Durant, Type: PlotToAssassinate
   Subject: Durant, Object: Claire, Type: FakesDeath
   Subject: Claire, Object: France, Type: FleesTo
   Subject: Durant, Object: France, Type: LivesIn
   Subject: Claire, Object: President Petrov, Type: DealOn
   Subject: Claire, Object: Syria, Type: DealOn
   Subject: Claire, Object: Durant, Type: DiscoversAlive
   Subject: Claire, Object: France, Type: WithPetrovHelp
   Subject: Claire, Object: Usher, Type: PlanToRemove
   Subject: Usher, Object: Claire, Type: PlanFoiled
   Subject: Claire, Object: Usher, Type: Fires
   Subject: Cabinet, Object: Annette, Type: ConsistsOf
   Subject: Annette, Object: Claire, Type: Conflict
   Subject: Annette, Object: Duncan, Type: FamilyConflict
   Subject: Claire, Object: Cabinet, Type: Leads
   Subject: Shepherds, Object: Claire, Type: Opposes
   Subject: Shepherds, Object: Brett Cole, Type: Enlists
   Subject: Shepherds, Object: Doug, Type: Enlists
   Subject: Brett Cole, Object: Speaker of the House, Type: AspiresTo
   Subject: Doug, Object: Hammerschmidt, Type: MeetsWith
   Subject: Doug, Object: Frank, Type: ProvidesInformationOn
   Subject: Claire, Object: Usher, Type: FramesFor
   Subject: Usher, Object: Yates, Type: AccusesOfMurder
   Subject: Claire, Object: Russia, Type: HasConnectionWith
   Subject: Claire, Object: Hammerschmidt, Type: HasKilled
   Subject: Claire, Object: Davis, Type: HasKilled
   Subject: Claire, Object: Durant, Type: HasKilled
   Subject: Claire, Object: Doug, Type: HasRevealedTo
   Subject: Claire, Object: Frank, Type: HasChildWith
   Subject: Claire, Object: maiden name, Type: RevertsTo
   Subject: Claire, Object: progressive agenda, Type: Continues
   Subject: Annette, Object: Bill, Type: StrainedFrom
   Subject: Annette, Object: Usher, Type: PlotsWith
   Subject: Usher, Object: Vice President, Type: NoLonger
   Subject: Annette, Object: Claire, Type: Assassinate
   Subject: Annette, Object: Usher, Type: Assassinate
   Subject: Annette, Object: Doug, Type: AsksTo
   Subject: Doug, Object: reluctant, Type: Is
   Subject: Doug, Object: Frank, Type: DesiringToProtect
   Subject: Claire, Object: Cole, Type: Through
   Subject: Claire, Object: Justice Abruzzo, Type: Blackmails
   Subject: Justice Abruzzo, Object: recusing, Type: Into
   Subject: Justice Abruzzo, Object: case, Type: In
   Subject: Claire, Object: launch nuclear weapons, Type: DealingWith
   Subject: Janine Skorsky, Object: Doug, Type: WorkToUncover
   Subject: Doug, Object: Frank, Type: Leaks
   Subject: Claire, Object: Frank, Type: Blames
   Subject: Claire, Object: ICO, Type: CreatesCrisis
   Subject: Shepherds, Object: Doug, Type: AcceleratesPlans
   Subject: Doug, Object: Claire, Type: Visits
   Subject: Doug, Object: Frank, Type: Kills
   Subject: Doug, Object: Frank, Type: UnderminesLegacy
   Subject: Doug, Object: Claire, Type: Threatens
   Subject: Doug, Object: Claire, Type: Wounds
   Subject: Claire, Object: Doug, Type: Stabs
   Subject: Claire, Object: Doug, Type: Suffocates
   Subject: Claire, Object: Janine Skorsky, Type: UnawareOf
   """,
                query=f"Based on the relationship information below, answer question: {text_query}"
            )
            st.write(ans)






