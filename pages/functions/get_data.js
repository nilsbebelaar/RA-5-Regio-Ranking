export async function onRequest(context) {
    let data = await context.env.VIJF_REGIO_KV.get("main_ranking");
    return new Response(data);
  }