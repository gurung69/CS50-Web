document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Sending email
  document.querySelector('#submit').addEventListener('click', ()=>{
    const reciver = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    fetch('/emails', {
      method:'POST',
      body:JSON.stringify({
        recipients:reciver,
        subject:subject,
        body:body
      })
    })

    load_mailbox('sent');
    return false;
  })

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // load mailbox
  fetch(`emails/${mailbox}`)
  .then(res => res.json())
  .then(emails => {
    emails.forEach(email => {
      const pv = document.createElement('div');
      pv.classList.add('email-pv');
      pv.dataset.id = email.id
      pv.innerHTML = `
      <div class='email-pv-info'>
        <h4>${email.sender}</h4>
        <span>${email.timestamp}</span>
      </div>
      <div>${email.subject}</div>`

      if (email.read){
        pv.style.background = '#ababab';
      }
      
      // view email
      pv.addEventListener('click',()=>{
        fetch(`/emails/${pv.dataset.id}`)
        .then(res=>res.json())
        .then(email=>{
          document.querySelector('#emails-view').innerHTML = `
            <div>
              <p><span>From:</span> ${email.sender}</p>
              <p><span>To:</span> ${email.recipients}</p>
              <p><span>Subject:</span> ${email.subject}</p>
              <p><span>Timestamp:</span> ${email.timestamp}</p>
              <button class="btn btn-primary" id='reply'>Reply</button>
              <hr>
              <textarea class="form-control" disabled>${email.body}</textarea>
              <hr>
            </div>`
          
          if (mailbox != 'sent'){
            if (email.archived){
              document.querySelector('#emails-view').innerHTML += `<button class="btn btn-primary" id='tg-archived'>Unarchive</button>`
            }
            else{
              document.querySelector('#emails-view').innerHTML += `<button class="btn btn-primary" id='tg-archived'>Archive</button>`
            }
          }
          document.querySelector('#reply').addEventListener('click', ()=>{
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'block';

            document.querySelector('#compose-recipients').value = email.sender
            if (email.subject.slice(0,4) != 'Re: '){
              document.querySelector('#compose-subject').value = `Re: ${email.subject}`
            }
            else{
              document.querySelector('#compose-subject').value = email.subject
            }

            document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`
          })
          document.querySelector('#tg-archived').addEventListener('click',()=>{
            console.log(email)
            fetch(`emails/${pv.dataset.id}`,{
              method:'PUT',
              body:JSON.stringify({
                archived:!email.archived
              })
            })
            location.reload()
          })
        })

        fetch(`/emails/${pv.dataset.id}`,{
          method:'PUT',
          body:JSON.stringify({
            read:true
          })
        })
      })

      document.querySelector('#emails-view').append(pv)
    });
  });
}