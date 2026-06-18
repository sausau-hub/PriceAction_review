/**
 * 直接用 CDP 读取 TradingView ES1! 月线/日线数据，并截图保存
 * 用于补充 2025-04-21 分析 markdown
 */
import CDP from 'chrome-remote-interface';
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const SCREENSHOT_DIR = 'D:\\AI视频\\AI分析视频\\screenshots';
const CHART_API = 'window.TradingViewApi._activeChartWidgetWV.value()';

async function findChartTarget() {
  const resp = await fetch('http://localhost:9222/json/list');
  const targets = await resp.json();
  return targets.find(t => t.type === 'page' && /tradingview\.com\/chart/i.test(t.url))
    || targets.find(t => t.type === 'page' && /tradingview/i.test(t.url))
    || null;
}

async function evaluate(client, expression) {
  const result = await client.Runtime.evaluate({
    expression,
    returnByValue: true,
    awaitPromise: false,
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  }
  return result.result?.value;
}

async function evaluateAsync(client, expression) {
  const result = await client.Runtime.evaluate({
    expression,
    returnByValue: true,
    awaitPromise: true,
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  }
  return result.result?.value;
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function screenshot(client, filename) {
  const { data } = await client.Page.captureScreenshot({ format: 'png' });
  mkdirSync(SCREENSHOT_DIR, { recursive: true });
  const filePath = join(SCREENSHOT_DIR, filename);
  writeFileSync(filePath, Buffer.from(data, 'base64'));
  console.log(`截图已保存: ${filePath}`);
  return filePath;
}

async function getChartState(client) {
  return evaluate(client, `
    (function() {
      var chart = ${CHART_API};
      return {
        symbol: chart.symbol(),
        resolution: chart.resolution(),
      };
    })()
  `);
}

async function setSymbol(client, symbol) {
  await evaluateAsync(client, `
    (function() {
      var chart = ${CHART_API};
      return new Promise(function(resolve) {
        chart.setSymbol(${JSON.stringify(symbol)}, {});
        setTimeout(resolve, 2000);
      });
    })()
  `);
  await sleep(1500);
}

async function setTimeframe(client, tf) {
  await evaluate(client, `
    (function() {
      var chart = ${CHART_API};
      chart.setResolution(${JSON.stringify(tf)}, {});
    })()
  `);
  await sleep(2000);
}

async function scrollToDate(client, dateStr) {
  const ts = Math.floor(new Date(dateStr).getTime() / 1000);
  await evaluate(client, `
    (function() {
      var chart = ${CHART_API};
      chart.setVisibleRange({ from: ${ts - 86400 * 365 * 2}, to: ${ts + 86400 * 30} }, {});
    })()
  `);
  await sleep(1500);
}

async function getOhlcv(client, count = 30) {
  return evaluate(client, `
    (function() {
      try {
        var chart = ${CHART_API};
        var series = chart._chartWidget.model().mainSeries();
        var bars = series.bars();
        var result = [];
        var len = bars.size();
        var start = Math.max(0, len - ${count});
        for (var i = start; i < len; i++) {
          var b = bars.get(i);
          if (!b) continue;
          var t = b.time;
          result.push({
            time: t,
            date: new Date(t * 1000).toISOString().slice(0, 10),
            open: b.value[1],
            high: b.value[2],
            low: b.value[3],
            close: b.value[4],
            volume: b.value[5],
          });
        }
        return result;
      } catch(e) {
        return { error: e.message };
      }
    })()
  `);
}

async function main() {
  const target = await findChartTarget();
  if (!target) { console.error('未找到 TradingView 图表窗口'); process.exit(1); }
  console.log(`连接目标: ${target.title} (${target.id})`);

  const client = await CDP({ host: 'localhost', port: 9222, target: target.id });
  await client.Runtime.enable();
  await client.Page.enable();

  // 先获取当前状态
  const state = await getChartState(client);
  console.log('当前图表状态:', JSON.stringify(state));

  // ===== 月线 =====
  console.log('\n--- 切换到 ES1! 月线 ---');
  await setSymbol(client, 'ES1!');
  await setTimeframe(client, 'M');
  await scrollToDate(client, '2025-04-21');

  const monthlyState = await getChartState(client);
  console.log('月线状态:', JSON.stringify(monthlyState));

  const monthlyOhlcv = await getOhlcv(client, 24);
  console.log('\n月线 OHLCV (最近24棒):');
  if (Array.isArray(monthlyOhlcv)) {
    monthlyOhlcv.forEach(b => {
      console.log(`${b.date}  O:${b.open?.toFixed(2)} H:${b.high?.toFixed(2)} L:${b.low?.toFixed(2)} C:${b.close?.toFixed(2)}`);
    });
  } else {
    console.log(JSON.stringify(monthlyOhlcv));
  }

  const monthlyScreenshot = await screenshot(client, 'ES1_Monthly_2025-04-21.png');

  // ===== 日线 =====
  console.log('\n--- 切换到 日线 ---');
  await setTimeframe(client, 'D');
  await scrollToDate(client, '2025-04-21');
  await sleep(1000);

  const dailyOhlcv = await getOhlcv(client, 40);
  console.log('\n日线 OHLCV (最近40棒):');
  if (Array.isArray(dailyOhlcv)) {
    dailyOhlcv.forEach(b => {
      console.log(`${b.date}  O:${b.open?.toFixed(2)} H:${b.high?.toFixed(2)} L:${b.low?.toFixed(2)} C:${b.close?.toFixed(2)}`);
    });
  } else {
    console.log(JSON.stringify(dailyOhlcv));
  }

  const dailyScreenshot = await screenshot(client, 'ES1_Daily_2025-04-21.png');

  // ===== 60分钟线 =====
  console.log('\n--- 切换到 60分钟线 ---');
  await setTimeframe(client, '60');
  await scrollToDate(client, '2025-04-21');
  await sleep(1000);

  const h1Ohlcv = await getOhlcv(client, 48);
  console.log('\n60分钟 OHLCV:');
  if (Array.isArray(h1Ohlcv)) {
    h1Ohlcv.forEach(b => {
      console.log(`${b.date}  O:${b.open?.toFixed(2)} H:${b.high?.toFixed(2)} L:${b.low?.toFixed(2)} C:${b.close?.toFixed(2)}`);
    });
  } else {
    console.log(JSON.stringify(h1Ohlcv));
  }

  const h1Screenshot = await screenshot(client, 'ES1_60min_2025-04-21.png');

  await client.close();

  console.log('\n=== 完成 ===');
  console.log('月线截图:', monthlyScreenshot);
  console.log('日线截图:', dailyScreenshot);
  console.log('60分钟截图:', h1Screenshot);

  // 输出 JSON 供后续处理
  writeFileSync('D:\\AI视频\\AI分析视频\\chart_data.json', JSON.stringify({
    monthly: monthlyOhlcv,
    daily: dailyOhlcv,
    h1: h1Ohlcv,
  }, null, 2));
  console.log('数据已保存到 chart_data.json');
}

main().catch(e => { console.error('错误:', e); process.exit(1); });
