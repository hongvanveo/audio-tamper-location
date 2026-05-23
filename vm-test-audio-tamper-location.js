const fs = require("fs");
const path = require("path");
const { Client } = require("ssh2");

const host = "192.168.72.134";
const username = "student";
const password = "password123";
const lab = "audio-tamper-location";
const localLab = path.join(__dirname, lab);
const remoteLabs = "/home/student/labtainer/trunk/labs";
const remoteLab = `${remoteLabs}/${lab}`;
const env =
  "export DISPLAY=:0 LABTAINER_DIR=/home/student/labtainer/trunk " +
  "PATH=/home/student/labtainer/trunk/scripts/labtainer-student/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin";

function connect() {
  return new Promise((resolve, reject) => {
    const conn = new Client();
    conn.on("ready", () => resolve(conn)).on("error", reject).connect({
      host,
      username,
      password,
      readyTimeout: 15000,
    });
  });
}

function exec(conn, command, timeoutMs = 120000) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`timeout: ${command}`)), timeoutMs);
    conn.exec(command, (err, stream) => {
      if (err) {
        clearTimeout(timer);
        reject(err);
        return;
      }
      let stdout = "";
      let stderr = "";
      stream.on("close", (code) => {
        clearTimeout(timer);
        resolve({ code, stdout, stderr });
      });
      stream.on("data", (data) => (stdout += data.toString()));
      stream.stderr.on("data", (data) => (stderr += data.toString()));
    });
  });
}

function sftp(conn) {
  return new Promise((resolve, reject) => {
    conn.sftp((err, client) => (err ? reject(err) : resolve(client)));
  });
}

function mkdir(client, remote) {
  return new Promise((resolve, reject) => {
    client.mkdir(remote, (err) => {
      if (err && err.code !== 4) reject(err);
      else resolve();
    });
  });
}

function fastPut(client, local, remote) {
  return new Promise((resolve, reject) => {
    client.fastPut(local, remote, (err) => (err ? reject(err) : resolve()));
  });
}

async function uploadDir(client, localDir, remoteDir) {
  await mkdir(client, remoteDir);
  for (const entry of fs.readdirSync(localDir, { withFileTypes: true })) {
    if (entry.name === "__pycache__" || entry.name === ".git") continue;
    const localPath = path.join(localDir, entry.name);
    const remotePath = `${remoteDir}/${entry.name}`;
    if (entry.isDirectory()) {
      await uploadDir(client, localPath, remotePath);
    } else if (entry.isFile()) {
      await fastPut(client, localPath, remotePath);
    }
  }
}

async function main() {
  const conn = await connect();
  try {
    console.log(`upload ${lab}`);
    await exec(conn, `mkdir -p ${remoteLabs} && rm -rf ${remoteLab}`);
    const client = await sftp(conn);
    await uploadDir(client, localLab, remoteLab);
    client.end();
    await exec(conn, `chmod +x ${remoteLab}/instr_config/pregrade.sh ${remoteLab}/student/stego/*.py`);

    console.log("rebuild");
    let res = await exec(
      conn,
      `cd /home/student/labtainer/labtainer-student && ${env} && yes B22DCAT311 | rebuild ${lab}`,
      900000
    );
    console.log(res.stdout);
    console.error(res.stderr);
    console.log(`rebuild_exit=${res.code}`);
    if (res.code !== 0) process.exitCode = res.code;

    console.log("start lab");
    res = await exec(
      conn,
      `cd /home/student/labtainer/labtainer-student && ${env} && stoplab ${lab} >/dev/null 2>&1 || true; printf 'B22DCAT311\\n' | labtainer -r ${lab} >/tmp/${lab}_start.log 2>&1; cat /tmp/${lab}_start.log`,
      240000
    );
    console.log(res.stdout);
    console.error(res.stderr);
    console.log(`start_exit=${res.code}`);
    if (res.code !== 0) process.exitCode = res.code;

    console.log("do lab tasks inside container");
    res = await exec(
      conn,
      `docker exec -u ubuntu ${lab}.student.student /bin/sh -c "cd /home/ubuntu/stego && python3 generate_cover.py --out cover.wav --seconds 5 && printf 'fragile audio signature\\n' > sign.txt && perl -0pi -e 's/AUDIO_FILE = \\"\\"/AUDIO_FILE = \\"cover.wav\\"/; s/SIGN_FILE = \\"\\"/SIGN_FILE = \\"sign.txt\\"/' embed_task.py && python3 embed_task.py && cp verify_task.py verify_marked.py && perl -0pi -e 's/AUDIO_FILE = \\"\\"/AUDIO_FILE = \\"marked.wav\\"/; s/SIGN_FILE = \\"\\"/SIGN_FILE = \\"sign.txt\\"/' verify_marked.py && python3 verify_marked.py && printf 'tamper this region\\n' > message.txt && perl -0pi -e 's/AUDIO_FILE = \\"\\"/AUDIO_FILE = \\"marked.wav\\"/; s/MESSAGE_FILE = \\"\\"/MESSAGE_FILE = \\"message.txt\\"/' tamper_task.py && python3 tamper_task.py && cp verify_task.py verify_tampered.py && perl -0pi -e 's/AUDIO_FILE = \\"\\"/AUDIO_FILE = \\"tampered.wav\\"/; s/SIGN_FILE = \\"\\"/SIGN_FILE = \\"sign.txt\\"/' verify_tampered.py && python3 verify_tampered.py && python3 refresh_status.py && cat /home/ubuntu/.local/result/tamper_location_check.txt"`,
      240000
    );
    console.log(res.stdout);
    console.error(res.stderr);
    console.log(`task_exit=${res.code}`);
    if (res.code !== 0) process.exitCode = res.code;

    console.log("final checkwork");
    res = await exec(
      conn,
      `cd /home/student/labtainer/labtainer-student && ${env} && checkwork 2>&1`,
      120000
    );
    console.log(res.stdout);
    console.error(res.stderr);
    console.log(`final_check_exit=${res.code}`);
    if (res.code !== 0) process.exitCode = res.code;
  } finally {
    conn.end();
  }
}

main().catch((err) => {
  console.error(err.stack || err.message);
  process.exit(1);
});
