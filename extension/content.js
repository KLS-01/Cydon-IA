window.onload = function () {
  // Aggiungi lo stile NES.css
  const linkElement = document.createElement('link');
  linkElement.rel = 'stylesheet';
  linkElement.href = 'https://unpkg.com/nes.css@latest/css/nes.min.css';
  document.head.appendChild(linkElement);

  // Collega i font da Google Fonts
  const linkElement2 = document.createElement('link');
  linkElement2.rel = 'preconnect';
  linkElement2.href = 'https://fonts.googleapis.com';
  document.head.appendChild(linkElement2);

  const linkElement3 = document.createElement('link');
  linkElement3.rel = 'preconnect';
  linkElement3.href = 'https://fonts.gstatic.com';
  document.head.appendChild(linkElement3);

  const linkElement4 = document.createElement('link');
  linkElement4.rel = 'stylesheet';
  linkElement4.href = 'https://fonts.googleapis.com/css2?family=Silkscreen:wght@400;700&display=swap';
  document.head.appendChild(linkElement4);

  // Aggiungi il link alla libreria Font Awesome
  const linkElement5 = document.createElement('link');
  linkElement5.rel = 'stylesheet';
  linkElement5.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css';
  document.head.appendChild(linkElement5);

  // Attendi che gli elementi siano presenti nel DOM
  const checkExist = setInterval(function () {
    const parentDiv = document.querySelector('.ps-room.ps-room-opaque');
    const battleControlsDiv = document.querySelector('.battle-controls');
    const battleLogDiv = document.querySelector('.battle-log');

    if (parentDiv && battleControlsDiv) {
      clearInterval(checkExist);
    }

    // Modifica lo stile dei battle controls
    if (battleControlsDiv) {
      battleControlsDiv.style.position = 'static';
      battleControlsDiv.style.display = 'flex';
      battleControlsDiv.style.background = 'none';
      battleControlsDiv.style.paddingBottom = '10px';
    }

    // Modifica lo stile dei bottoni nella cydonia interface
    if (battleLogDiv) {
      battleLogDiv.style.left = '660px';
    }

    // Aggiungi un observer per la cydonia interface
    const observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        const cydoniaInterfaceDiv = document.querySelector('.cydonia-interface');
        if (!cydoniaInterfaceDiv) {
          // Creazione del div principale per la Cydon-IA
          const cydoniaDiv = document.createElement('div');
          cydoniaDiv.className = 'cydonia-interface';
          parentDiv.insertBefore(cydoniaDiv, battleControlsDiv);
          cydoniaDiv.appendChild(battleControlsDiv);

          // Creazione della sezione per la Cydon-IA
          const sectionCydonIA = document.createElement('section');
          sectionCydonIA.className = 'nes-container with-title';
          const titleSection = document.createElement('h3');
          titleSection.className = 'title';
          titleSection.textContent = 'Cydon-IA';
          sectionCydonIA.appendChild(titleSection);
          // TODO:
          let responseSection = document.createElement('h1');
          responseSection.id = 'cydonia-result';
          sectionCydonIA.appendChild(responseSection);

          // Creazione del pulsante per la Cydon-IA
          const buttonReloadCydonIA = document.createElement('button');
          buttonReloadCydonIA.id = 'cydonia-button';
          buttonReloadCydonIA.className = 'nes-btn';
          buttonReloadCydonIA.style.margin = '5px 5px 5px 5px';
          buttonReloadCydonIA.style.borderImageRepeat = 'stretch';
          const iconaRicarica = document.createElement('i');
          iconaRicarica.className = 'fas fa-sync-alt';
          buttonReloadCydonIA.appendChild(iconaRicarica);

          // Creazione del div per la user interface di Cydon-IA
          const userInterfaceDiv = document.createElement('div');
          userInterfaceDiv.style.display = 'flex';
          userInterfaceDiv.style.flexDirection = 'row';
          userInterfaceDiv.style.flexFlow = 'row';

          // Aggiunta della sezione alla user interface di Cydon-IA
          userInterfaceDiv.appendChild(sectionCydonIA);

          // Aggiunta del pulsante alla user interface di Cydon-IA
          userInterfaceDiv.appendChild(buttonReloadCydonIA);

          // Aggiunta della user Interface di Cydon-IA al div principale della Cydon-IA
          cydoniaDiv.appendChild(userInterfaceDiv);

          // Assegna una funzionalità al pulsante per la Cydon-IA
          document.getElementById('cydonia-button').addEventListener('click', cydoniaClick);
        }

        if (cydoniaInterfaceDiv && battleControlsDiv) {
          const topValue = window.getComputedStyle(battleControlsDiv).getPropertyValue('top');
          cydoniaInterfaceDiv.style.top = topValue;

          const buttonsInCydoniaInterface = cydoniaInterfaceDiv.querySelectorAll('.button');
          buttonsInCydoniaInterface.forEach(button => {
            button.classList.remove('button');
            button.classList.add('nes-btn');
            button.style.borderImageRepeat = 'stretch';
          });
        }
      });
    });

    observer.observe(parentDiv, { childList: true, subtree: true });
  }, 100);
};

function cydoniaClick() {
  let pkmn1 = getPokemonInfo(1);
  let pkmn2 = getPokemonInfo(2);

  let request = {};

  request.pokemon1 = pkmn1;
  request.pokemon2 = pkmn2;

  let xhr = new XMLHttpRequest();
  xhr.open("POST", "http://localhost:5000/api/ia/cydonia", true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.status === 200) {
      const response = JSON.parse(xhr.responseText);
      let suggest = document.getElementById('cydonia-result');
      if(response.best_move == '0') {
        suggest.textContent = 'ATTACK'
      } else {
        suggest.textContent = 'DEFEND'
      }
    } else {
      console.error('Error:', xhr.statusText);
    }
  }

  xhr.send(JSON.stringify(request));
  xhr.close;
}

function getPokemonInfo(n_pkmn) {
  let pkmn;

  switch (n_pkmn) {
    case 1:
      let name_pkm1 = document.querySelector('.statbar.rstatbar.leftstatbar strong').textContent;

      let hp_pkm1_tmp = document.querySelector('.statbar.rstatbar').textContent;
      let hp_pkm1_tmp2 = hp_pkm1_tmp.replace(name_pkm1, "");
      let hp_pkm1 = hp_pkm1_tmp2.split('%')[0];

      let statbarElement1 = document.querySelector('.statbar.rstatbar');
      let statusElement1 = statbarElement1.querySelector('.status');
      let has_status1 = statusElement1 && statusElement1.querySelector('span:not(.good)') !== null;
      let has_boost1 = statusElement1 && statusElement1.querySelector('span.good') !== null;

      let switchmenuElement = document.querySelector('.switchmenu');
      let buttonElements = switchmenuElement.querySelectorAll('button');
      let allButtonsHaveChooseDisabled = Array.from(buttonElements).every(button => button.getAttribute('name') === 'chooseDisabled');
      let can_switch1 = !allButtonsHaveChooseDisabled;
      pkmn = {
        name: name_pkm1,
        hp: hp_pkm1,
        has_status: has_status1,
        has_boost: has_boost1,
        can_switch: can_switch1
      };
      break;

    case 2:
      let name_pkm2 = document.querySelector('.statbar.lstatbar.leftstatbar strong').textContent;

      let hp_pkm2_tmp = document.querySelector('.statbar.lstatbar').textContent;
      let hp_pkm2_tmp2 = hp_pkm2_tmp.replace(name_pkm2, "");
      let hp_pkm2 = hp_pkm2_tmp2.split('%')[0];

      let statbarElement2 = document.querySelector('.statbar.lstatbar');
      let statusElement2 = statbarElement2.querySelector('.status');
      let has_status2 = statusElement2 && statusElement2.querySelector('span:not(.good)') !== null;
      let has_boost2 = statusElement2 && statusElement2.querySelector('span.good') !== null;
      pkmn = {
        name: name_pkm2,
        hp: hp_pkm2,
        has_status: has_status2,
        has_boost: has_boost2,
        can_switch: null
      };
      break;

    default:
      console.log("Value not valid: there are just Pokemon1 and Pokemon2 on the field!");
  }

  return pkmn;
}
