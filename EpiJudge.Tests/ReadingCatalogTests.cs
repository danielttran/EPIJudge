using System.Text.Json;
using EpiJudge.Web;

namespace EpiJudge.Tests;

public class ReadingCatalogTests
{
    private const string Id = "reading-shared-state";
    private static string Document(string notes = "notes λ", bool reviewed = true) => JsonSerializer.Serialize(new
    {
        version = 1, notes, reviewed, checkpoints = new[] { "contract" }, answers = new { understanding = 0 }
    });

    [Fact]
    public void ReadingDocumentsCanBeBackedUpWithoutBecomingAcceptedSubmissions()
    {
        var draft = new Draft(Id, "reading", Document(), 1, "2026-10-19T00:00:00Z");
        Assert.True(ReadingCatalog.ValidDocument(Id, draft.Code));
        Assert.True(PracticeBackupValidator.Validate(new(1, [draft], [], []), _ => false));
        Assert.False(PracticeBackupValidator.Validate(new(1, [draft], [], [Id]), _ => false));
        Assert.False(PracticeEndpoints.ValidLanguage("reading"));
    }

    [Theory]
    [InlineData("null")]
    [InlineData("invalid")]
    [InlineData("{}")]
    [InlineData("{\"version\":\"1\"}")]
    [InlineData("{\"version\":1,\"notes\":\"\",\"reviewed\":true,\"checkpoints\":[],\"answers\":{\"understanding\":99}}")]
    [InlineData("{\"version\":1,\"notes\":\"\",\"reviewed\":true,\"checkpoints\":[\"unknown\"],\"answers\":{}}")]
    [InlineData("{\"version\":1,\"notes\":\"\",\"reviewed\":true,\"checkpoints\":[],\"answers\":{\"unknown\":0}}")]
    public void MalformedOrUnknownReadingWorkIsRejected(string code) => Assert.False(ReadingCatalog.ValidDocument(Id, code));

    [Fact]
    public void NotesHaveTheirOwnLimitAndSupportEscapedUnicode()
    {
        Assert.True(ReadingCatalog.ValidDocument(Id, Document(new string('\u0001', 20_000))));
        Assert.False(ReadingCatalog.ValidDocument(Id, Document(new string('x', 20_001))));
        Assert.False(ReadingCatalog.ValidDocument("count_bits", Document()));
        Assert.False(ReadingCatalog.ValidDocument(Id, null));
    }
}
