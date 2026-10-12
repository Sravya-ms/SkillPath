(function () {
  // skill chips (resume review): click a chip to remove it, type to add
  var box = document.getElementById('chips');
  if (box) {
    var hidden = document.getElementById('skills-input'), input = document.getElementById('chip-new');
    var skills = hidden.value ? hidden.value.split(',').filter(Boolean) : [];
    var render = function () {
      box.innerHTML = '';
      skills.forEach(function (s, i) {
        var c = document.createElement('button');
        c.type = 'button'; c.className = 'chip'; c.textContent = s + ' \u00d7';
        c.onclick = function () { skills.splice(i, 1); render(); };
        box.appendChild(c);
      });
      hidden.value = skills.join(',');
    };
    var add = function () {
      var v = input.value.trim().toLowerCase();
      if (v && skills.indexOf(v) < 0) skills.push(v);
      input.value = ''; render();
    };
    document.getElementById('chip-add').onclick = add;
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); add(); } });
    render();
  }
  // scan animation on upload
  var up = document.getElementById('upload-form');
  if (up) up.addEventListener('submit', function () { document.getElementById('drop').classList.add('scanning'); });
  // dashboard chart
  var cv = document.getElementById('scores'), data = document.getElementById('chart-data');
  if (cv && data && window.Chart) {
    var d = JSON.parse(data.textContent);
    new Chart(cv, {type: 'bar', data: {labels: d.map(function (x) { return x.label; }),
      datasets: [{label: 'Exam score %', data: d.map(function (x) { return x.score; }), backgroundColor: '#35D0BA'}]},
      options: {scales: {y: {min: 0, max: 100}}}});
  }
})();
