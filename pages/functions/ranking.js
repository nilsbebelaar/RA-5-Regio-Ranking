export async function onRequest(context) {
    // Create a prepared statement with our query
    const ps = context.env.VIJF_REGIO_DB.prepare('SELECT * from regio_ranking');
    const data = await ps.first();
  
    return Response.json(data);
  }