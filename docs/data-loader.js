// Static data transport for hosts that isolate documents with an opaque origin.
// These companions preserve audited JSON/gzip bytes and need no external host.
(() => {
  const pending = new Map();
  function load(path) {
    if (!/^data\/[a-zA-Z0-9_./-]+$/.test(path) || path.includes('..'))
      return Promise.reject(new Error('Invalid data path.'));
    if (pending.has(path)) return pending.get(path).promise;
    const request = {}, script = document.createElement('script');
    request.promise = new Promise((resolve, reject) => {
      let complete = false;
      const finish = error => {
        if (complete) return;
        complete = true;
        clearTimeout(timer);
        script.remove();
        pending.delete(path);
        if (error) { reject(error); return; }
        try {
          if (typeof request.encoded !== 'string') throw new Error('The data file returned no payload.');
          resolve(Uint8Array.from(atob(request.encoded), c => c.charCodeAt(0)));
        } catch (error) { reject(error); }
        request.encoded = null;
      };
      const timer = setTimeout(() => finish(new Error('Loading data timed out. Please reload the page.')), 60000);
      script.onload = () => finish();
      script.onerror = () => finish(new Error('Could not load ' + path + '. Please refresh the artifact mirror.'));
      script.src = path + '.js';
    });
    pending.set(path, request);
    document.head.append(script);
    return request.promise;
  }
  globalThis.LUMEN_DATA = Object.freeze({
    load,
    register(path, encoded) { const request = pending.get(path); if (request) request.encoded = encoded; },
  });
})();
