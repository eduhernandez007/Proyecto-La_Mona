class Match {
  constructor({ sport, teamA, teamB, scoreA, scoreB, status, venue, referee, teamAMembers, teamBMembers }) {
    this.sport = sport;
    this.teamA = teamA;
    this.teamB = teamB;
    this.scoreA = scoreA;
    this.scoreB = scoreB;
    this.status = status;
    this.venue = venue;
    this.referee = referee;
    this.teamAMembers = teamAMembers;
    this.teamBMembers = teamBMembers;
  }

  static parseMembers(value) {
    return String(value || '')
      .split(',')
      .map(name => name.trim())
      .filter(Boolean);
  }

  static fromInput(data) {
    return new Match({
      sport: data.sport || 'Deporte',
      teamA: data.teamA || 'Equipo A',
      teamB: data.teamB || 'Equipo B',
      scoreA: Number.parseInt(data.scoreA, 10) || 0,
      scoreB: Number.parseInt(data.scoreB, 10) || 0,
      status: data.status || 'Programado',
      venue: data.venue || 'Lugar pendiente',
      referee: data.referee || 'No designado',
      teamAMembers: Match.parseMembers(data.teamAMembers),
      teamBMembers: Match.parseMembers(data.teamBMembers),
    });
  }

  formatMembers(members) {
    return members.join(', ');
  }
}

class MatchManager {
  constructor(initialMatches = []) {
    this.matches = initialMatches.map(match => new Match(match));
  }

  get count() {
    return this.matches.length;
  }

  get(index) {
    return this.matches[index] || null;
  }

  add(match) {
    this.matches.push(new Match(match));
  }

  update(index, match) {
    if (this.matches[index]) {
      this.matches[index] = new Match(match);
    }
  }
}

class AuthManager {
  constructor(users, initialUser = { name: 'Visitante', role: 'invitado' }) {
    this.users = users;
    this.currentUser = initialUser;
  }

  login(username, password) {
    const account = this.users[username];
    if (account && account.password === password) {
      this.currentUser = { name: account.label, role: account.role };
      return true;
    }
    return false;
  }

  logout() {
    this.currentUser = { name: 'Visitante', role: 'invitado' };
  }

  get role() {
    return this.currentUser.role;
  }

  get label() {
    return this.currentUser.name;
  }

  isOrganizer() {
    return this.role === 'organizador';
  }

  isCompetitionOrganizer() {
    return this.role === 'organizador_competencia';
  }

  isJudge() {
    return this.role === 'juez';
  }

  isStudentCenter() {
    return this.role === 'centro';
  }

  isPlayer() {
    return this.role === 'jugador';
  }

  canAddMatch() {
    return this.isOrganizer();
  }

  canEditMatch() {
    return this.isOrganizer() || this.isCompetitionOrganizer() || this.isJudge();
  }

  canEditFullMatch() {
    return this.isOrganizer() || this.isCompetitionOrganizer();
  }

  canEditResults() {
    return this.isOrganizer() || this.isCompetitionOrganizer() || this.isJudge();
  }
}

class SportsApp {
  constructor() {
    this.storageKey = 'sportsAppData';
    const savedState = this.loadState();

    this.elements = {
      matchList: document.getElementById('matchList'),
      matchCount: document.getElementById('matchCount'),
      accessNote: document.getElementById('accessNote'),
      saveMatchButton: document.getElementById('saveMatchButton'),
      newMatchButton: document.getElementById('newMatchButton'),
      addMatchButton: document.getElementById('addMatchButton'),
      adminControlsTitle: document.getElementById('adminControlsTitle'),
      sportInput: document.getElementById('sportInput'),
      teamAInput: document.getElementById('teamAInput'),
      teamBInput: document.getElementById('teamBInput'),
      teamAMembersInput: document.getElementById('teamAMembersInput'),
      teamBMembersInput: document.getElementById('teamBMembersInput'),
      refereeInput: document.getElementById('refereeInput'),
      scoreAInput: document.getElementById('scoreAInput'),
      scoreBInput: document.getElementById('scoreBInput'),
      statusInput: document.getElementById('statusInput'),
      venueInput: document.getElementById('venueInput'),
      adminControls: document.getElementById('adminControls'),
      loginOverlay: document.getElementById('loginOverlay'),
      userNameInput: document.getElementById('userNameInput'),
      passwordInput: document.getElementById('passwordInput'),
      loginButton: document.getElementById('confirmLoginButton'),
      openLoginButton: document.getElementById('openLoginButton'),
      logoutButton: document.getElementById('logoutButton'),
      loginError: document.getElementById('loginError'),
      loggedUser: document.getElementById('loggedUser'),
      loggedRole: document.getElementById('loggedRole'),
      playerActions: document.getElementById('playerActions'),
      requestEnrollmentButton: document.getElementById('requestEnrollmentButton'),
      playerRequestForm: document.getElementById('playerRequestForm'),
      requestCompetitionInput: document.getElementById('requestCompetitionInput'),
      requestDepartmentInput: document.getElementById('requestDepartmentInput'),
      submitRequestButton: document.getElementById('submitRequestButton'),
      cancelRequestButton: document.getElementById('cancelRequestButton'),
      playerRequestStatus: document.getElementById('playerRequestStatus'),
      studentCenterSection: document.getElementById('studentCenterSection'),
      requestsList: document.getElementById('requestsList'),
      playerList: document.getElementById('playerList'),
      studentCenterEdit: document.getElementById('studentCenterEdit'),
      editPlayerTitle: document.getElementById('editPlayerTitle'),
      editPlayerNameInput: document.getElementById('editPlayerNameInput'),
      editPlayerDepartmentInput: document.getElementById('editPlayerDepartmentInput'),
      editPlayerCompetitionsInput: document.getElementById('editPlayerCompetitionsInput'),
      savePlayerButton: document.getElementById('savePlayerButton'),
      cancelPlayerEditButton: document.getElementById('cancelPlayerEditButton'),
    };

    this.userInputs = [
      this.elements.sportInput,
      this.elements.teamAInput,
      this.elements.teamBInput,
      this.elements.teamAMembersInput,
      this.elements.teamBMembersInput,
      this.elements.refereeInput,
      this.elements.scoreAInput,
      this.elements.scoreBInput,
      this.elements.statusInput,
      this.elements.venueInput,
    ];

    this.auth = new AuthManager(savedState?.users || users);
    this.matchManager = new MatchManager(savedState?.matches || matches);
    this.enrollmentRequests = savedState?.enrollmentRequests || [];
    this.players = savedState?.players || [
      { name: 'Juan Pérez', department: 'Derecho', competitions: ['Fútbol'] },
      { name: 'María López', department: 'Ciencias', competitions: ['Básquet'] },
      { name: 'Sergio Martín', department: 'Ingeniería', competitions: ['Tenis'] },
    ];
    this.editingPlayerIndex = null;
    this.editingIndex = null;
  }

  init() {
    this.bindEvents();
    this.updateLoginState();
    this.renderMatches();
    this.saveState();
  }

  bindEvents() {
    this.elements.loginButton.addEventListener('click', () => this.handleLogin());
    this.elements.openLoginButton.addEventListener('click', () => this.openLogin());
    this.elements.logoutButton.addEventListener('click', () => this.handleLogout());
    this.elements.userNameInput.addEventListener('keydown', event => {
      if (event.key === 'Enter') this.handleLogin();
    });
    this.elements.passwordInput.addEventListener('keydown', event => {
      if (event.key === 'Enter') this.handleLogin();
    });
    this.elements.saveMatchButton.addEventListener('click', () => this.saveMatch());
    this.elements.newMatchButton.addEventListener('click', () => this.hideAdminControls());
    this.elements.addMatchButton.addEventListener('click', () => this.openAddMatchForm());
    this.elements.requestEnrollmentButton.addEventListener('click', () => this.openPlayerRequestForm());
    this.elements.submitRequestButton.addEventListener('click', () => this.submitEnrollmentRequest());
    this.elements.cancelRequestButton.addEventListener('click', () => this.closePlayerRequestForm());
    this.elements.savePlayerButton.addEventListener('click', () => this.savePlayerEdit());
    this.elements.cancelPlayerEditButton.addEventListener('click', () => this.cancelPlayerEdit());
  }

  createMatchCard(match, index) {
    const card = document.createElement('article');
    card.className = 'match-item';

    card.innerHTML = `
      <div class="match-item-header">
        <div>
          <h3>${match.sport}</h3>
          <p class="match-venue">${match.venue}</p>
        </div>
        <button class="edit-button">Editar</button>
      </div>
      <div class="match-score">
        <strong>${match.teamA}</strong>
        <span>${match.scoreA} - ${match.scoreB}</span>
        <strong>${match.teamB}</strong>
      </div>
      <div class="match-meta">
        <p><strong>Estado:</strong> ${match.status}</p>
        <p><strong>Árbitro:</strong> ${match.referee}</p>
      </div>
      <div class="match-teams">
        <div>
          <h4>${match.teamA}</h4>
          <p>${match.formatMembers(match.teamAMembers)}</p>
        </div>
        <div>
          <h4>${match.teamB}</h4>
          <p>${match.formatMembers(match.teamBMembers)}</p>
        </div>
      </div>
    `;

    const editButton = card.querySelector('.edit-button');
    editButton.addEventListener('click', () => this.selectMatch(index));

    if (!this.auth.canEditMatch()) {
      editButton.classList.add('hidden');
    }

    return card;
  }

  renderMatches() {
    this.elements.matchList.innerHTML = '';
    this.matchManager.matches.forEach((match, index) => {
      this.elements.matchList.appendChild(this.createMatchCard(match, index));
    });
    this.elements.matchCount.textContent = `${this.matchManager.count} partido${this.matchManager.count === 1 ? '' : 's'}`;
  }

  populateForm(match) {
    this.elements.sportInput.value = match.sport;
    this.elements.teamAInput.value = match.teamA;
    this.elements.teamBInput.value = match.teamB;
    this.elements.scoreAInput.value = match.scoreA;
    this.elements.scoreBInput.value = match.scoreB;
    this.elements.statusInput.value = match.status;
    this.elements.venueInput.value = match.venue;
    this.elements.refereeInput.value = match.referee;
    this.elements.teamAMembersInput.value = match.formatMembers(match.teamAMembers);
    this.elements.teamBMembersInput.value = match.formatMembers(match.teamBMembers);
  }

  resetForm() {
    this.editingIndex = null;
    this.elements.sportInput.value = '';
    this.elements.teamAInput.value = '';
    this.elements.teamBInput.value = '';
    this.elements.scoreAInput.value = '';
    this.elements.scoreBInput.value = '';
    this.elements.statusInput.value = '';
    this.elements.venueInput.value = '';
    this.elements.refereeInput.value = '';
    this.elements.teamAMembersInput.value = '';
    this.elements.teamBMembersInput.value = '';
  }

  showAdminControls(title) {
    this.elements.adminControlsTitle.textContent = title;
    this.elements.adminControls.classList.remove('hidden');
    this.elements.addMatchButton.classList.toggle('hidden', !this.auth.canAddMatch());
  }

  hideAdminControls() {
    this.resetForm();
    this.elements.adminControls.classList.add('hidden');
  }

  selectMatch(index) {
    const match = this.matchManager.get(index);
    if (!match) return;
    this.editingIndex = index;
    this.populateForm(match);
    this.showAdminControls('Editar partido');
    this.configureInputsForRole();
  }

  saveMatch() {
    const inputData = {
      sport: this.elements.sportInput.value,
      teamA: this.elements.teamAInput.value,
      teamB: this.elements.teamBInput.value,
      scoreA: this.elements.scoreAInput.value,
      scoreB: this.elements.scoreBInput.value,
      status: this.elements.statusInput.value,
      venue: this.elements.venueInput.value,
      referee: this.elements.refereeInput.value,
      teamAMembers: this.elements.teamAMembersInput.value,
      teamBMembers: this.elements.teamBMembersInput.value,
    };

    if (this.auth.isOrganizer()) {
      const match = Match.fromInput(inputData);
      if (this.editingIndex === null) {
        this.matchManager.add(match);
      } else {
        this.matchManager.update(this.editingIndex, match);
      }
      this.renderMatches();
      this.hideAdminControls();
      this.saveState();
      return;
    }

    if (this.auth.isCompetitionOrganizer()) {
      if (this.editingIndex === null) {
        alert('Solo el organizador principal puede agregar partidos. Selecciona un partido existente para editarlo.');
        return;
      }
      const match = Match.fromInput(inputData);
      this.matchManager.update(this.editingIndex, match);
      this.renderMatches();
      this.hideAdminControls();
      this.saveState();
      return;
    }

    if (this.auth.isJudge()) {
      if (this.editingIndex === null) {
        alert('Selecciona un partido para registrar o modificar el resultado.');
        return;
      }
      const currentMatch = this.matchManager.get(this.editingIndex);
      if (currentMatch) {
        currentMatch.scoreA = Number.parseInt(this.elements.scoreAInput.value, 10) || 0;
        currentMatch.scoreB = Number.parseInt(this.elements.scoreBInput.value, 10) || 0;
        currentMatch.status = this.elements.statusInput.value || currentMatch.status;
      }
      this.renderMatches();
      this.hideAdminControls();
      this.saveState();
      return;
    }

    alert('No tienes permisos para modificar partidos en este rol.');
  }

  updateLoginState() {
    const role = this.auth.role;
    this.elements.loggedUser.textContent = this.auth.label;
    this.elements.loggedRole.textContent =
      role === 'organizador' ? 'Organizador' :
      role === 'organizador_competencia' ? 'Organizador de competencia' :
      role === 'juez' ? 'Juez' :
      role === 'centro' ? 'Centro de estudiantes' :
      role === 'jugador' ? 'Jugador' :
      'Invitado';

    if (this.auth.isOrganizer()) {
      this.elements.accessNote.textContent = 'Eres organizador. Tienes acceso completo al sistema.';
      this.elements.accessNote.classList.remove('access-note--warning');
      this.elements.addMatchButton.classList.remove('hidden');
      this.hideAdminControls();
    } else if (this.auth.isCompetitionOrganizer()) {
      this.elements.accessNote.textContent = 'Eres organizador de competencia. Puedes administrar encuentros y participantes en tu competencia.';
      this.elements.accessNote.classList.remove('access-note--warning');
      this.elements.addMatchButton.classList.add('hidden');
      this.hideAdminControls();
    } else if (this.auth.isJudge()) {
      this.elements.accessNote.textContent = 'Eres juez. Puedes registrar y modificar resultados en tu competencia.';
      this.elements.accessNote.classList.remove('access-note--warning');
      this.elements.addMatchButton.classList.add('hidden');
      this.hideAdminControls();
    } else if (this.auth.isStudentCenter()) {
      this.elements.accessNote.textContent = 'Eres centro de estudiantes. Puedes revisar jugadores, equipos y solicitudes de tu departamento.';
      this.elements.accessNote.classList.remove('access-note--warning');
      this.elements.addMatchButton.classList.add('hidden');
      this.elements.adminControls.classList.add('hidden');
      this.elements.playerActions.classList.add('hidden');
      this.elements.studentCenterSection.classList.remove('hidden');
      this.hideAdminControls();
      this.renderEnrollmentRequests();
      this.renderPlayersList();
    } else if (this.auth.isPlayer()) {
      this.elements.accessNote.textContent = 'Eres jugador. Puedes ver tus participaciones y solicitar inscripciones.';
      this.elements.accessNote.classList.remove('access-note--warning');
      this.elements.addMatchButton.classList.add('hidden');
      this.elements.adminControls.classList.add('hidden');
      this.elements.playerActions.classList.remove('hidden');
      this.elements.studentCenterSection.classList.add('hidden');
      this.elements.playerRequestForm.classList.add('hidden');
      this.hideAdminControls();
    } else {
      this.elements.accessNote.textContent = 'Solo el organizador principal puede agregar/modificar partidos. El resultado es visible para todos.';
      this.elements.accessNote.classList.add('access-note--warning');
      this.elements.addMatchButton.classList.add('hidden');
      this.elements.adminControls.classList.add('hidden');
      this.elements.playerActions.classList.add('hidden');
      this.elements.studentCenterSection.classList.add('hidden');
      this.elements.playerRequestForm.classList.add('hidden');
    }

    this.elements.openLoginButton.classList.toggle('hidden', role !== 'invitado');
    this.elements.logoutButton.classList.toggle('hidden', role === 'invitado');

    this.elements.openLoginButton.classList.toggle('hidden', role !== 'invitado');
    this.elements.logoutButton.classList.toggle('hidden', role === 'invitado');

    this.configureInputsForRole();
    this.renderMatches();
  }

  handleLogin() {
    const username = this.elements.userNameInput.value.trim().toLowerCase();
    const password = this.elements.passwordInput.value;
    if (this.auth.login(username, password)) {
      this.elements.loginOverlay.classList.add('hidden');
      this.elements.loginError.classList.add('hidden');
      this.updateLoginState();
    } else {
      this.elements.loginError.classList.remove('hidden');
    }
  }

  openLogin() {
    this.elements.loginOverlay.classList.remove('hidden');
  }

  openPlayerRequestForm() {
    this.elements.playerRequestForm.classList.remove('hidden');
    this.elements.playerRequestStatus.classList.add('hidden');
    this.elements.requestCompetitionInput.value = '';
    this.elements.requestDepartmentInput.value = '';
  }

  closePlayerRequestForm() {
    this.elements.playerRequestForm.classList.add('hidden');
    this.elements.playerRequestStatus.classList.add('hidden');
  }

  submitEnrollmentRequest() {
    const competition = this.elements.requestCompetitionInput.value.trim();
    const department = this.elements.requestDepartmentInput.value.trim();
    if (!competition || !department) {
      this.elements.playerRequestStatus.textContent = 'Por favor completa competencia y departamento.';
      this.elements.playerRequestStatus.classList.remove('hidden');
      return;
    }

    this.enrollmentRequests.push({
      id: Date.now(),
      player: this.auth.label,
      competition,
      department,
      status: 'Pendiente',
    });

    this.elements.playerRequestStatus.textContent = 'Solicitud enviada. El centro de estudiantes la revisará pronto.';
    this.elements.playerRequestStatus.classList.remove('hidden');
    this.elements.requestCompetitionInput.value = '';
    this.elements.requestDepartmentInput.value = '';
    this.elements.playerRequestForm.classList.add('hidden');
    this.saveState();
  }

  openAddMatchForm() {
    this.resetForm();
    this.editingIndex = null;
    this.showAdminControls('Agregar partido');
    this.configureInputsForRole();
  }

  configureInputsForRole() {
    this.userInputs.forEach(input => {
      if (this.auth.isOrganizer() || this.auth.isCompetitionOrganizer()) {
        input.disabled = false;
      } else if (this.auth.isJudge()) {
        const editable = input === this.elements.scoreAInput ||
          input === this.elements.scoreBInput ||
          input === this.elements.statusInput;
        input.disabled = !editable;
      } else {
        input.disabled = true;
      }
    });
  }

  renderEnrollmentRequests() {
    if (!this.elements.requestsList) return;
    this.elements.requestsList.innerHTML = '';
    if (this.enrollmentRequests.length === 0) {
      this.elements.requestsList.innerHTML = '<p>No hay solicitudes pendientes.</p>';
      return;
    }

    this.enrollmentRequests.forEach((request, index) => {
      const item = document.createElement('article');
      item.className = 'request-item';
      item.innerHTML = `
        <div>
          <p><strong>Jugador:</strong> ${request.player}</p>
          <p><strong>Competencia:</strong> ${request.competition}</p>
          <p><strong>Departamento:</strong> ${request.department}</p>
          <p><strong>Estado:</strong> ${request.status}</p>
        </div>
        <div class="request-actions">
          <button class="secondary-button approve-request">Aprobar</button>
          <button class="secondary-button reject-request">Rechazar</button>
        </div>
      `;
      const approveButton = item.querySelector('.approve-request');
      const rejectButton = item.querySelector('.reject-request');
      approveButton.addEventListener('click', () => this.updateRequestStatus(index, 'Aprobada'));
      rejectButton.addEventListener('click', () => this.updateRequestStatus(index, 'Rechazada'));
      this.elements.requestsList.appendChild(item);
    });
  }

  updateRequestStatus(requestIndex, status) {
    const request = this.enrollmentRequests[requestIndex];
    if (!request) return;
    request.status = status;
    if (status === 'Aprobada') {
      this.players.push({
        name: request.player,
        department: request.department,
        competitions: [request.competition],
      });
    }
    this.renderEnrollmentRequests();
    this.renderPlayersList();
    this.saveState();
  }

  renderPlayersList() {
    if (!this.elements.playerList) return;
    this.elements.playerList.innerHTML = '';
    if (this.players.length === 0) {
      this.elements.playerList.innerHTML = '<p>No hay jugadores registrados.</p>';
      return;
    }

    this.players.forEach((player, index) => {
      const row = document.createElement('article');
      row.className = 'player-item';
      row.innerHTML = `
        <div>
          <p><strong>${player.name}</strong></p>
          <p>${player.department}</p>
          <p>${player.competitions.join(', ')}</p>
        </div>
        <button class="secondary-button edit-player">Editar</button>
      `;
      const editButton = row.querySelector('.edit-player');
      editButton.addEventListener('click', () => this.editPlayer(index));
      this.elements.playerList.appendChild(row);
    });
  }

  editPlayer(index) {
    const player = this.players[index];
    if (!player) return;
    this.editingPlayerIndex = index;
    this.elements.editPlayerTitle.textContent = `Editar jugador: ${player.name}`;
    this.elements.editPlayerNameInput.value = player.name;
    this.elements.editPlayerDepartmentInput.value = player.department;
    this.elements.editPlayerCompetitionsInput.value = player.competitions.join(', ');
    this.elements.studentCenterEdit.classList.remove('hidden');
  }

  savePlayerEdit() {
    if (this.editingPlayerIndex === null) return;
    const player = this.players[this.editingPlayerIndex];
    if (!player) return;
    player.name = this.elements.editPlayerNameInput.value.trim() || player.name;
    player.department = this.elements.editPlayerDepartmentInput.value.trim() || player.department;
    player.competitions = Match.parseMembers(this.elements.editPlayerCompetitionsInput.value);
    this.elements.studentCenterEdit.classList.add('hidden');
    this.editingPlayerIndex = null;
    this.renderPlayersList();
    this.saveState();
  }

  cancelPlayerEdit() {
    this.editingPlayerIndex = null;
    this.elements.studentCenterEdit.classList.add('hidden');
  }

  handleLogout() {
    this.auth.logout();
    this.elements.loginOverlay.classList.add('hidden');
    this.updateLoginState();
    this.resetForm();
  }

  saveState() {
    const state = {
      matches: this.matchManager.matches,
      players: this.players,
      enrollmentRequests: this.enrollmentRequests,
      users,
    };
    localStorage.setItem(this.storageKey, JSON.stringify(state));
  }

  loadState() {
    try {
      const raw = localStorage.getItem(this.storageKey);
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      console.warn('No se pudo cargar el estado guardado:', error);
      return null;
    }
  }
}

const users = {
  organizador: { password: '1234', role: 'organizador', label: 'Organizador' },
  organizador_competencia: { password: '1234', role: 'organizador_competencia', label: 'Organizador de competencia' },
  juez: { password: '1234', role: 'juez', label: 'Juez' },
  centro: { password: '1234', role: 'centro', label: 'Centro de estudiantes' },
  jugador: { password: '1234', role: 'jugador', label: 'Jugador' },
};

const matches = [
  {
    sport: 'Fútbol',
    teamA: 'Club Campeón',
    teamB: 'Rival FC',
    scoreA: 2,
    scoreB: 1,
    status: 'Finalizado',
    venue: 'Estadio Central',
    referee: 'Carlos Pérez',
    teamAMembers: ['Juan', 'María', 'Carlos'],
    teamBMembers: ['Luis', 'Ana', 'Pedro'],
  },
  {
    sport: 'Básquet',
    teamA: 'Tigres',
    teamB: 'Halcones',
    scoreA: 88,
    scoreB: 82,
    status: 'Finalizado',
    venue: 'Arena Norte',
    referee: 'Marta Ríos',
    teamAMembers: ['Pablo', 'Sofía', 'Raúl'],
    teamBMembers: ['Diego', 'Camila', 'Nora'],
  },
  {
    sport: 'Tenis',
    teamA: 'Sergio',
    teamB: 'Martina',
    scoreA: 3,
    scoreB: 2,
    status: 'En curso',
    venue: 'Cancha Central',
    referee: 'Lucía Gómez',
    teamAMembers: ['Sergio'],
    teamBMembers: ['Martina'],
  },
];

const app = new SportsApp();
app.init();
