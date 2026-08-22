const http = require("http");

const server = http.createServer((req, res) => {
  const method = req.method;
  const url = (req.url || "").split("?")[0];

  // @endpoint GET /delay/5
  if (method === "GET" && url === "/delay/5") {
    const body = {
      args: {},
      data: "",
      files: {},
      form: {},
      headers: {
        Accept: "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        Host: "httpbin.org",
        "User-Agent": "PostmanRuntime/2.3.4"
      },
      origin: "91.107.179.103",
      url: "https://httpbin.org/delay/5"
    };
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(body, null, 2));
    return;
  }

  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: "Not found" }));
});

server.listen(process.env.PORT || 3000);