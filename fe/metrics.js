import express from "express";
import { collectDefaultMetrics, Counter, register } from "prom-client";

const app = express();
const port = 3002;

collectDefaultMetrics();

const requestCounter = new Counter({
  name: "http_requests_total",
  help: "Total number of HTTP requests",
  labelNames: ["method", "status_code"],
});

app.get("/", (req, res) => {
  requestCounter.inc({ method: req.method, status_code: res.statusCode });
  res.send("Hello World!");
});

app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

app.listen(port, () => {
  console.log("Metrics server running");
});
