## VULNERABLE SQUID
Vulnerable squid is an <b>Intentionally Vulnerable Web Application(IVWA)</b> that is meant for penetration testing practice and simulation. 
This is a Docker image that you have to compose in order to run the application.
  
Some of the attacks possible include:
1. XSS
2. CSRF
3. SQLInjection

This project uses Python, with the Flask web framework.
The backend of the application uses nginx 1.15.0 and MySQL 5.7

---

### How to run
You need to have docker installed to run this project. Refer to the 
<a href="https://docs.docker.com/engine/install/">official Docker documentation </a>
on how to install docker for your system.
  
1. Clone this repository
```shell
  git clone https://github.com/yeajxn/vulnerable-squid
```
2. You can build the docker image with the docker compose file.
```shell
   docker compose up --build
```
