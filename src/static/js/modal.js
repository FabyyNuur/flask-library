    // Get all modal elements
    var modals = document.getElementsByClassName("modal");
    var modals2 = document.getElementsByClassName("modal2");
    // Get all button elements to open modals
    var btns = document.getElementsByClassName("openModalBtn");
    var btns2 = document.getElementsByClassName("openModalBtn2");
    // Get all close elements
    var spans = document.getElementsByClassName("close");
    var spans2 = document.getElementsByClassName("close2");

    function openModal(index) {
        modals[index].style.display = "block";
      }

      function openModal2(index) {
        modals2[index].style.display = "block";
      }

      function closeModal(index) {
        modals[index].style.display = "none";
      }
      function closeModal2(index) {
        modals2[index].style.display = "none";
      }

      for (var i = 0; i < btns.length; i++) {
        btns[i].addEventListener("click", function() {
          var index = Array.prototype.indexOf.call(btns, this);
          openModal(index);
        });
      }
      for (var i = 0; i < btns2.length; i++) {
        btns2[i].addEventListener("click", function() {
          var index = Array.prototype.indexOf.call(btns2, this);
          openModal2(index);
        });
      }

      for (var i = 0; i < spans.length; i++) {
        spans[i].addEventListener("click", function() {
          var index = Array.prototype.indexOf.call(spans, this);
          closeModal(index);
        });
      }

      for (var i = 0; i < spans2.length; i++) {
        spans2[i].addEventListener("click", function() {
          var index = Array.prototype.indexOf.call(spans2, this);
          closeModal2(index);
        });
      }

      window.addEventListener("click", function(event) {
        for (var i = 0; i < modals.length; i++) {
          if (event.target == modals[i]) {
            closeModal(i);
          }
        }
      });
      window.addEventListener("click", function(event) {
        for (var i = 0; i < modals2.length; i++) {
          if (event.target == modals2[i]) {
            closeModal2(i);
          }
        }
      });