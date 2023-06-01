export async function onRequest(context) {
    let data = await context.env.VIJF_REGIO_KV.get(context.params.key);
    return new Response(decodeURIComponent(data));
  }