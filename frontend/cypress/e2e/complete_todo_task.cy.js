describe('Todo list', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user
  let t_title // task title

  before( () => {
    cy.fixture('user.json')
    .then( (user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid
        name = user.firstName + ' ' + user.lastName
        email = user.email
        cy.visit('http://localhost:3000')
        cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)
        cy.get('form').submit();
        cy.fixture('task.json')
        .then((task) => {
            t_title = task.title;
            cy.get('#title')
              .type(task.title);
            cy.get('#url')
              .type(task.url);
            cy.get('form')
              .submit();
            cy.contains(t_title)
              .click()
        });
      })
    })
  })

  beforeEach("login", () => {
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
    cy.get("form")
      .submit();
    cy.contains(t_title)
      .click();
  })

  it("todo set active -> done", () => {
    cy.get(".todo-item")
      .find(".checker")
      .should("have.class", "unchecked").click()
    .then(() => {
      cy.get(".checker")
        .should("have.class", "checked")
    });
  })

  it("todo set done -> active", () => {
    cy.get(".todo-item")
      .find(".editable")
      .invoke("css", "text-decoration")
      .should("include", "line-through");
    cy.get(".checker")
      .click();
    cy.get(".todo-item")
      .find(".editable")
      .invoke("css", "text-decoration")
      .should("include", "none");
  })

  after(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})