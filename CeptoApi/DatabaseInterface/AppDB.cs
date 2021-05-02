using System;
using System.Collections.Generic;
using System.Linq;
using MySqlConnector;

namespace CeptoApi.DatabaseInterface
{
    public sealed class AppDB : IDisposable
    {
        private readonly MySqlConnection conn;

        public AppDB(string host, UInt16 port, string uname, string passwd, string db)
        {
            conn = new MySqlConnection($"host={host};port={port};user id={uname};password={passwd};database={db}");
            conn.Open();
        }

        /// <summary>
        ///
        /// </summary>
        /// <returns>List of all active session tokens</returns>
        public List<Guid> get_all_session_tokens()
        {
            var session_tokens = new List<Guid>();

            using var cmd = new MySqlCommand("SELECT token from tokens;", conn);
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                var token = reader.GetGuid(1);
                session_tokens.Append(token);
            }

            return session_tokens;
        }

        public void add_session_token()
        {
            using (var cmd = new MySqlCommand("INSERT INTO users(full_name, age) VALUES('Kevork', 21);", conn))
                cmd.ExecuteNonQuery();
        }

        public List<Event> get_event_entries() {}

        public bool delete_all_expired_session_tokens()
        {
            return true;
        }
        // Guid
        // list of references to patients

        public void Dispose()
        {
            conn.Close();
        }
    }
}
