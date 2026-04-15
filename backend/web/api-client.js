/**
 * 为 /api/v1/* 请求自动附加 sessionStorage 中的 JWT（登录页写入 jyis_access_token）。
 * 健康检查等非 v1 接口仍请使用原生 fetch。
 */
window.jyisApiFetch = function (url, init) {
  init = init || {};
  var headers = new Headers(init.headers != null ? init.headers : undefined);
  try {
    var t = sessionStorage.getItem("jyis_access_token");
    if (t && !headers.has("Authorization")) {
      headers.set("Authorization", "Bearer " + t);
    }
  } catch (e) {}
  init.headers = headers;
  return fetch(url, init);
};

/**
 * 在 #userBar（或 opts.elementId）展示登录态：无 token 提示登录；有 token 则 GET …/auth/me。
 * 返回 { refresh } 供页面在登出后再次调用；首次调用会绑定退出/清除令牌按钮。
 */
window.jyisInitUserBar = function (opts) {
  opts = opts || {};
  var apiBase = opts.apiBase || "/api/v1";
  var elId = opts.elementId || "userBar";
  var el = document.getElementById(elId);
  if (!el) return null;

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  async function refresh() {
    var tok = null;
    try {
      tok = sessionStorage.getItem("jyis_access_token");
    } catch (e) {}
    if (!tok) {
      el.innerHTML = "未登录 · <a href=\"/ui/login.html\">登录</a>";
      return;
    }
    try {
      var r = await window.jyisApiFetch(apiBase + "/auth/me");
      if (!r.ok) throw new Error(String(r.status));
      var u = await r.json();
      el.innerHTML =
        "已登录 <strong>" +
        esc(u.email || "") +
        "</strong> " +
        "<button type=\"button\" class=\"secondary\" id=\"btnLogoutBar\" style=\"margin-left:0.35rem;padding:0.2rem 0.55rem;font-size:0.78rem\">退出</button>";
    } catch (e) {
      el.innerHTML =
        "<span class=\"err\">令牌无效或过期</span> · <a href=\"/ui/login.html\">重新登录</a> " +
        "<button type=\"button\" class=\"secondary\" id=\"btnClrTok\" style=\"margin-left:0.25rem;padding:0.2rem 0.55rem;font-size:0.78rem\">清除令牌</button>";
    }
  }

  if (!el.dataset.jyisUserbarInit) {
    el.dataset.jyisUserbarInit = "1";
    el.addEventListener("click", function (ev) {
      var t = ev.target;
      if (!t || t.nodeType !== 1) return;
      var id = t.id;
      if (id === "btnLogoutBar" || id === "btnClrTok") {
        try {
          sessionStorage.removeItem("jyis_access_token");
          sessionStorage.removeItem("jyis_refresh_token");
        } catch (e2) {}
        refresh();
      }
    });
  }

  refresh();
  return { refresh: refresh };
};
