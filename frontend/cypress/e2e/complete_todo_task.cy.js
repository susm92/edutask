describe('Todo list', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  let t_id;
  let t_title;
  let t_desc;
  let t_start;
  let t_due;
  let t_url;

  before(function () {
    cy.fixture("user.json")
      .then((user) => {
        cy.request({
          method: "POST",
          url: "http://localhost:5000/users/create",
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid;
          name = user.firstName + " " + user.lastName;
          email = user.email;
        })
      })
  })

  before(function () {
    cy.fixture("task.json")
      .then((task) => {
        task.userid = uid;
        cy.request({
          method: "POST",
          url: "http://localhost:5000/tasks/create",
          form: true,
          body: task
        }).then((response) => {
          console.log(response)
          t_id = response.body._id;
          t_title = task.title;
          t_desc = task.description;
          t_start = task.start;
          t_due = task.due;
          t_url = task.url;
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
    cy.get("img")
      .click({ force: true });
  })

  it("task set to done", () => {
      cy.get(".checker")
        .click();
      cy.get(".todo-item")
        .find(".editable")
        .invoke("css", "text-decoration")
        .should("include", "line-through");
  })

  it("task set done -> active", () => {
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